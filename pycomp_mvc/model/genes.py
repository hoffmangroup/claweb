__author__ = 'mickael'

import pandas as pd
import os


def gene_list(config_file, group_and_comparisons):

    datasets_genes = []
    datasets_name = ','.join([dataset['name'] for dataset in config_file['datasets']])

    for dataset in config_file['datasets']:
        df = pd.read_csv(dataset['summary'], sep='\t')
        df = df[(df.robustness == 10) & (df.accuracy > .9)]

        genes = df.gene.value_counts().keys().tolist()
        genes.sort(key=lambda x:x.split(':')[-1].lower())

        genes = [{"name": gene.split(':')[-1],"filename": gene + '.html'} for gene in genes]

        datasets_genes.append({'name': dataset['name'], 'genes': genes})

    return datasets_genes, datasets_name


def gene_card(config_file, group_and_comparisons, dataset, gene):

    groupid_to_name = {group['id']: group['name'] for group in group_and_comparisons['group_definitions']}

    df = pd.read_csv(dataset['summary'], sep='\t')
    df = df[(df.robustness == 10) & (df.accuracy > .9) & (df.gene == gene)]

    groups = []
    for group in group_and_comparisons['group_definitions']:

        group_df = df[(df.cl1 == group['id']) | (df.cl2 == group['id'])]

        if group_df.empty:
            continue

        rows = group_df[['cl1', 'cl2', 't-test', 'p-value']].values.tolist()
        rows.sort(key=lambda x: abs(x[2]), reverse=True)
        rows = [[groupid_to_name[group1], groupid_to_name[group2], ttest, pval] for group1, group2, ttest, pval in rows]

        up_in_cl1_count = group_df[(group_df['t-test'] > 0) & (group_df['cl1'] == group['id'])].shape[0]
        up_in_cl2_count = group_df[(group_df['t-test'] <= 0) & (group_df['cl2'] == group['id'])].shape[0]
        down_in_cl1_count = group_df[(group_df['t-test'] <= 0) & (group_df['cl1'] == group['id'])].shape[0]
        down_in_cl2_count = group_df[(group_df['t-test'] > 0) & (group_df['cl2'] == group['id'])].shape[0]


        groups.append({'name': group['name'],
                       'rows': rows,
                       'up_count': up_in_cl1_count + up_in_cl2_count,
                       'down_count': down_in_cl1_count + down_in_cl2_count})

    groups.sort(key=lambda x: x['up_count'] + x['down_count'], reverse=True)

    d = {"name": gene.split(':')[-1],
         "infos": groups,
         "dataset": dataset['name'],
         "coordinates": gene,
         }

    gene_dist_url = os.path.join(config_file['website']['url'], 'gene_distribution', dataset['name'], gene)

    return d, gene_dist_url
