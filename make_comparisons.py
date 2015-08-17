__author__ = 'mickael'

from skrrf.ensemble import RegularizedRandomForestClassifier
# from pycomp.website.main import main as website_main

import argparse
import csv
import pandas as pd
import numpy as np
from scipy import stats
import os
import sys
import yaml


def ttest(S, groups):

    S = S.fillna(0.)

    g1_index = groups[groups == 0].index
    g2_index = groups[groups == 1].index

    return stats.ttest_ind(S[g1_index], S[g2_index])


def summarize(config_file):

    with open(config_file) as yaml_file:
        cgf = yaml.load(yaml_file)

    header = ['id',	'cl1', 'cl2', 'gene', 'robustness', 'accuracy', 't-test', 'p-value', 'p_row']

    for dataset in cgf['datasets']:
        rows = []

        path, folder, files = os.walk(dataset['output']).next()
        files = [f for f in files if not f.startswith('.')]

        #read and store the results
        for f in files:
            with open(os.path.join(path, f)) as tsvfile:
                reader = csv.reader(tsvfile, delimiter='\t')
                reader.next() #skip header

                rows += [line for line in reader]

        #write the summary file
        summary_dir = "/".join(dataset['summary'].split('/')[:-1])

        if not os.path.exists(summary_dir):
            os.makedirs(summary_dir)

        with open(dataset['summary'], 'w') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            writer.writerow(header)
            writer.writerows(rows)


def run_all(config_file, comp_file):


    with open(config_file) as yaml_file:
        cgf = yaml.load(yaml_file)

    with open(comp_file) as yaml_file:
        group_and_comparisons = yaml.load(yaml_file)

    for dataset in cgf['datasets']:
        print dataset['name']

        expression_table = pd.read_csv(dataset['expression_table'], sep='\t', index_col=0)
        for comparison in group_and_comparisons['comparisons']:

            samples1 = [group['samples'] for group in group_and_comparisons['group_definitions'] if group['id'] == comparison['group1']][0]
            samples2 = [group['samples'] for group in group_and_comparisons['group_definitions'] if group['id'] == comparison['group2']][0]

            try:
                samples1 = [[s for s in expression_table.columns if sample in s][0] for sample in samples1]
                samples2 = [[s for s in expression_table.columns if sample in s][0] for sample in samples2]
            except:
                print "Samples defined in the comp_file do not match the samples in the expression table"
                print "Can not find the following pattern in the expression table: ", sample

            cur_expression_table = expression_table[samples1 + samples2]

            # print 'samp1, samp2', len(samples1), len(samples2)

            g1_min = cur_expression_table[samples1].min(1)
            g1_max = cur_expression_table[samples1].max(1)
            g2_min = cur_expression_table[samples2].min(1)
            g2_max = cur_expression_table[samples2].max(1)

            p1 = cur_expression_table.loc[g1_min > g2_max].index
            p2 = cur_expression_table.loc[g2_min > g1_max].index
            perfect_rows = p1.union(p2)

            expression_table_filtered = cur_expression_table.loc[cur_expression_table.index.difference(perfect_rows)]
            y = pd.Series([0 if s in samples1 else 1 for s in expression_table_filtered.columns])

            results = pd.DataFrame(index=expression_table_filtered.index)
            accuracys = []

            expression_table_filtered = expression_table_filtered.T

            print 'start', comparison['id']

            for i in range(10):
                rrf = RegularizedRandomForestClassifier(n_estimators=int(dataset['n_tree']), oob_score=True)
                accuracys.append(rrf.fit(expression_table_filtered.values, y.values).oob_score_)
                results[i] = rrf.feature_importances_

            gene_count = (results > 0).sum(1).order()

            rows = []

            for gene, count in gene_count[gene_count > 0].iteritems():
                tstat, pvalue = ttest(cur_expression_table.loc[gene], y)
                rows.append([comparison['id'], comparison['group1'], comparison['group2'],
                             gene, count, np.mean(accuracys), tstat, pvalue, 0])

            for gene in perfect_rows:
                tstat, pvalue = ttest(cur_expression_table.loc[gene], y)
                rows.append([comparison['id'], comparison['group1'], comparison['group2'],
                             gene, 10, np.mean(accuracys), tstat, pvalue, 1])

            if not os.path.exists(dataset['output']):
                os.makedirs(dataset['output'])

            header = ['id', 'cl1', 'cl2', 'gene', 'robustness', 'accuracy', 't-test', 'p-value', 'p_row']

            pd.DataFrame(rows, columns=header).to_csv(os.path.join(dataset['output'], str(comparison['id'])), index=False, sep='\t')

    summarize(config_file)
    # website_main(config_file, comp_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Regularized Random Forest.')
    parser.add_argument('--config_file', type=str, help='full path to the config file', required=True)
    parser.add_argument('--comp_file', type=str, help='full path to the comparison file', required=True)

    args = parser.parse_args(sys.argv[1:])

    run_all(args.config_file, args.comp_file)