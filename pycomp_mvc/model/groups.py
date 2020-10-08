"""
Created on Oct 7, 2013

@author: mmendez
"""
import json
import pandas as pd
import yaml
import os
from jinja2 import Environment, FileSystemLoader


def group(config_file, group_and_comparisons, group_id):

    header = []
    genes_counts = []

    group = [group for group in group_and_comparisons['group_definitions'] if group_id == group['id']][0]

    for dataset in config_file['datasets']:
        df = pd.read_csv(dataset['summary'], sep='\t')
        df = df[(df.robustness == 10) & (df.accuracy > .9) & ((df.cl1 == group_id) | (df.cl2 == group_id))]

        indexes_to_remove = []
        for _id, rows in df.groupby("id"):
            for gene, rows2 in rows.groupby("gene"):
                if rows2.shape[0] > 1:
                    indexes_to_remove.append(rows2[rows2.p_row == 0].index.tolist()[0])

        df = df.drop(indexes_to_remove)
        header.append([dataset['name'], df.id.value_counts().size])
        gene_count = list(df.gene.value_counts().iteritems())
        genes_counts.append(gene_count)

    df = pd.DataFrame(genes_counts).T

    group['print_name']
    if "B cell" in group['print_name']:
        print("smth")

    group = {'id': group['id'],
             'name': group['name'],
             'print_id': group['print_id'],
             'print_name': group['print_name'],
             'header': header,
             'rows': df.applymap(lambda x: ('', '') if pd.isnull(x) else x).values.tolist(),
             }

    return group

    
def group_list(config_file, group_and_comparisons):
    datasets = []

    for dataset in config_file['datasets']:
        df = pd.read_csv(dataset['summary'], sep='\t')
        df = df[(df.robustness == 10) & (df.accuracy > .9)]
        datasets.append(df)

    groups = []

    for group in group_and_comparisons['group_definitions']:
        nb_of_comps = []
        nb_of_genes = []

        for df in datasets:
            nb_of_comps.append(df[(df.cl1 == group['id']) | (df.cl2 == group['id'])].id.value_counts().size)
            nb_of_genes.append(df[(df.cl1 == group['id']) | (df.cl2 == group['id'])].gene.value_counts().size)

        if not max(nb_of_comps):
            continue

        groups.append({
            'name': group['name'],
            'print_name': group['print_name'],
            'link': os.path.join(config_file['website']['url'], 'groups', group['print_id'] + '.html'),
            'nb_of_comp': max(nb_of_comps),
            'gene_count': nb_of_genes
        })

    return sorted(groups, key=lambda x: x['print_name'])
