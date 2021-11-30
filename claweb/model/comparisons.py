__author__ = 'mickael'

import os
from collections import defaultdict

import pandas as pd


def comparison_url(cfg, comp_id):
    return os.path.join(cfg['website']['url'], 'comparisons', str(comp_id) + '.html')


def gene_dist_url(cfg, dataset_name, gene):
    return os.path.join(cfg['website']['url'], 'gene_distribution', dataset_name, gene)


def comparison_list(config_file, group_and_comparisons):

    results = defaultdict(list)
    group_to_name = {group['id']: group['name'] for group in group_and_comparisons['group_definitions']}

    comparisons = group_and_comparisons['comparisons']
    reversed_comparisons = [{'id': comp['id'], 'group1': comp['group2'], 'group2': comp['group1']}
                            for comp in group_and_comparisons['comparisons']]

    all_comparisons = comparisons + reversed_comparisons

    for comp in all_comparisons:
        g1_name = group_to_name[comp['group1']]

        results[g1_name].append({
            'url': comparison_url(config_file, comp['id']),
            'group1': group_to_name[comp['group1']],
            'group2': group_to_name[comp['group2']]
        })
    results = {k: results[k] for k in sorted(results)}
    return results


def comparison(config_file, group_and_comparisons, comp_id):

    dataset_genes = []
    group_to_name = {group['id']: group['name'] for group in group_and_comparisons['group_definitions']}

    comp = [comp for comp in group_and_comparisons['comparisons'] if comp['id'] == comp_id][0]
    group1_name = group_to_name[comp['group1']]
    group2_name = group_to_name[comp['group2']]

    for dataset in config_file['datasets']:

        df = pd.read_csv(dataset['summary'], sep='\t')
        df = df[(df.robustness == 10) & (df.accuracy > .9) & (df.id == comp_id)]

        df['name1'] = df['cl1'].apply(lambda x: group_to_name[x])
        df['name2'] = df['cl2'].apply(lambda x: group_to_name[x])
        df['short_name'] = df['gene'].apply(lambda x: x.split(':')[-1])
        # df['gene_dist_url'] = [gene_dist_url(config_file, dataset['name'], gene) for gene in df['gene']]

        sort_by_abs_ttest_index = df['t-test'].abs().sort_values(ascending=False).index
        df = df.reindex(sort_by_abs_ttest_index)

        rows = df.T.to_dict().values()
        dataset_genes.append({'name': dataset['name'], 'n_genes': len(rows), 'rows': rows})

    return dataset_genes, group1_name, group2_name

