__author__ = 'mickael'

import argparse
import os
import sys
from collections import defaultdict
from itertools import combinations

import numpy as np
import pandas as pd
import sklearn
from scipy import stats
from skrrf._forest import RegularizedRandomForestClassifier
from . import extra



def hamming_distance(list1, list2):
    """calculate hamming distance between two Pandas.Series"""
    return sum(list1 != list2)


def ttest(S, groups):
    S = S.fillna(0.)

    g1_index = groups[groups == 0].index
    g2_index = groups[groups == 1].index

    return stats.ttest_ind(S[g1_index], S[g2_index])


def get_similar_genes(cur_expression_table, sample_mapper, n_rep=3):
    genes = cur_expression_table.index

    # pre-sort classes based on expression
    gene_to_sorted_classes_list = []
    for i in range(n_rep):
        gene_to_sorted_classes = {}
        for gene, row in cur_expression_table.iterrows():
            sorted_indexs = sklearn.utils.shuffle(row).sort_values().index
            sorted_classes = sorted_indexs.map(sample_mapper)
            gene_to_sorted_classes[gene] = sorted_classes
        gene_to_sorted_classes_list.append(gene_to_sorted_classes)

    similar_genes = defaultdict(list)
    tracker = set()

    first = genes[0]
    for gene_i, gene_j in combinations(genes, 2):
        if not first == gene_i:
            if gene_i in tracker:
                continue
            first = gene_i

        if gene_j in tracker:
            continue

        genes_are_similar = True
        for gene_to_sorted_classes in gene_to_sorted_classes_list:
            hamming_dist = hamming_distance(
                gene_to_sorted_classes[gene_i],
                gene_to_sorted_classes[gene_j])
            if hamming_dist >= 1:
                genes_are_similar = False
                break

        if genes_are_similar:
            similar_genes[gene_i].append(gene_j)
            tracker.add(gene_i)
            tracker.add(gene_j)

    return tracker, similar_genes


def get_perfect_rows(df, samples1, samples2):
    """Perfect rows have a threshold value that can perfectly separate the samples.
    For example, a row with values above 10 in `samples1` and values below 10 in `samples2` is a perfect row"""
    g1_min = df[samples1].min(1)
    g1_max = df[samples1].max(1)
    g2_min = df[samples2].min(1)
    g2_max = df[samples2].max(1)

    p1 = df.loc[g1_min > g2_max].index
    p2 = df.loc[g2_min > g1_max].index
    return p1.union(p2)


def run_one(config_file, comp_file, comp_id):
    cgf = extra.load_config(config_file)
    gac = extra.GAC(comp_file)

    comparison = gac.get_comp_from_id(comp_id)

    for dataset in cgf['datasets']:

        output_basename = os.path.join(dataset['output'], str(comparison['id']))
        if os.path.exists(output_basename + "_fi.tsv") and os.path.exists(output_basename + "_comp.tsv"):
            continue

        if not os.path.exists(dataset['output']):
            os.makedirs(dataset['output'])

        expression_table = pd.read_csv(dataset['expression_table'], sep='\t', index_col=0)

        samples1 = gac.get_samples_from_group_id(comparison['group1'])
        samples2 = gac.get_samples_from_group_id(comparison['group2'])

        try:
            samples1 = [[s for s in expression_table.columns if sample in s][0] for sample in samples1]
            samples2 = [[s for s in expression_table.columns if sample in s][0] for sample in samples2]
        except:
            print("Can not find the following pattern in the expression table: ", sample)

        sample_mapper = {s: 0 for s in samples1}
        sample_mapper.update({s: 1 for s in samples2})

        cur_expression_table = expression_table[samples1 + samples2]

        # remove genes with no variance
        cur_expression_table = cur_expression_table[cur_expression_table.var(1) != 0]

        # find perfect rows
        perfect_rows = get_perfect_rows(cur_expression_table, samples1, samples2)

        filtered_index = cur_expression_table.index.difference(perfect_rows)

        # find genes with same hamming distance
        tracker, similar_genes = get_similar_genes(cur_expression_table.loc[filtered_index], sample_mapper)

        # when genes are similar, only use one
        filtered_index = filtered_index.difference(
            list(tracker)).union(
            similar_genes.keys())

        expression_table_filtered = cur_expression_table.loc[filtered_index]
        y = pd.Series([sample_mapper[sample] for sample in cur_expression_table.columns])
        min_sample_count = min(len(samples1), len(samples2))

        results = pd.DataFrame(index=expression_table_filtered.index)
        accuracies = []

        expression_table_filtered = expression_table_filtered.T

        for i in range(10):
            rrf = RegularizedRandomForestClassifier(n_estimators=int(dataset['n_tree']), oob_score=True,
                                                    random_state=i, n_jobs=1, max_samples=min_sample_count * 2)
            rrf.stratified_down_sampling = True
            accuracies.append(rrf.fit(expression_table_filtered.values, y.values).oob_score_)
            results[i] = rrf.feature_importances_

        results.to_csv(os.path.join(dataset['output'], str(comparison['id']) + '_fi.tsv'), sep='\t')
        gene_count = (results > 0).sum(1).sort_values()

        rows = []

        for gene, count in gene_count[gene_count > 0].iteritems():
            for gene in [gene] + similar_genes[gene]:
                tstat, pvalue = ttest(cur_expression_table.loc[gene], y)
                rows.append([comparison['id'], comparison['group1'], comparison['group2'],
                             gene, count, np.mean(accuracies), tstat, pvalue, 0])

        for gene in perfect_rows:
            tstat, pvalue = ttest(cur_expression_table.loc[gene], y)
            rows.append([comparison['id'], comparison['group1'], comparison['group2'],
                         gene, 10, np.mean(accuracies), tstat, pvalue, 1])

        if not os.path.exists(dataset['output']):
            os.makedirs(dataset['output'])

        header = ['id', 'cl1', 'cl2', 'gene', 'robustness', 'accuracy', 't-test', 'p-value', 'p_row']
        comp_file_output = os.path.join(dataset['output'], str(comparison['id'])) + '_comp.tsv'

        df = pd.DataFrame(rows, columns=header)
        df.to_csv(comp_file_output, index=False, sep='\t')


def parse_args(args):
    parser = argparse.ArgumentParser(description='Regularized Random Forest for one comparison.')
    parser.add_argument('config_file', type=str, help='full path to the config file')
    parser.add_argument('comp_file', type=str, help='full path to the comparison file')
    parser.add_argument('comp_id', type=int, help='THe identifier of a comparison defined in the comp_file')

    return parser.parse_args(args)


def cli_run_single_comp(args=sys.argv[1:]):
    args = parse_args(args)
    run_one(args.config_file, args.comp_file, args.comp_id)


if __name__ == '__main__':
    cli_run_single_comp()
