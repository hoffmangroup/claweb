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
        genes.sort(key=lambda x: x.split(':')[-1].lower())

        genes = [{"name": gene.split(':')[-1],"filename": gene + '.html'} for gene in genes]

        datasets_genes.append({'name': dataset['name'], 'genes': genes})

    return datasets_genes, datasets_name


def gene_card(config_file, group_and_comparisons, dataset, gene):

    groupid_to_name = {group['id']: group['name'] for group in group_and_comparisons['group_definitions']}
    group_name_to_print_name = {group['name']: group['print_name'] for group in group_and_comparisons['group_definitions']}

    df = pd.read_csv(dataset['summary'], sep='\t')
    n_cl = len(set(df.cl1.tolist() + df.cl2.unique().tolist()))
    # ndf[(df.robustness == 10) & (df.accuracy > .9) & (df.gene == gene)]
    # df = df[(df.robustness == 10) & (df.accuracy > .9) & (df.gene == gene)]

    groups = []
    for group in group_and_comparisons['group_definitions']:

        group_df = df[(df.cl1 == group['id']) | (df.cl2 == group['id'])]
        n_comp = group_df.id.unique().size
        success_df = group_df[(group_df.robustness == 10) & (group_df.accuracy > .9) & (group_df.gene == gene)]

        if success_df.empty:
            continue

        rows = success_df[['cl1', 'cl2', 't-test', 'p-value']].values.tolist()
        rows.sort(key=lambda x: abs(x[2]), reverse=True)

        final_rows = []
        higher_in_this = 0
        higher_in_compared = 0

        for group1, group2, ttest, pval in rows:
            name1 = groupid_to_name[group1]
            name2 = groupid_to_name[group2]
            row_score = [0, 0]

            if name1 == group["name"]:
                this_cl = name1
                comparison_cl = name2
            else:
                this_cl = name2
                comparison_cl = name1

            if ttest >= 0:
                higher_in = name1
            else:
                higher_in = name2

            if higher_in == this_cl:
                higher_in_this += 1
                row_score[0] = 1
            else:
                higher_in_compared += 1
                row_score[1] = 1

            final_rows.append([group_name_to_print_name[comparison_cl]] + row_score)

        groups.append({'name': group['name'],
                       'print_name': group['print_name'],
                       'rows': final_rows,
                       'up_count': higher_in_this,
                       'down_count': higher_in_compared,
                       'neither': n_comp - higher_in_this - higher_in_compared},
                      )

    groups.sort(key=lambda x: x['up_count'] + x['down_count'], reverse=True)

    d = {
        "name": gene.split(':')[-1],
        "infos": groups,
        "dataset": dataset['name'],
        "coordinates": gene,
        'n_cl': n_cl
    }

    gene_dist_url = os.path.join(config_file['website']['url'], 'gene_distribution', dataset['name'], gene)

    return d, gene_dist_url
