__author__ = 'mickael'

import base64
import matplotlib.pyplot as plt
from io import StringIO
import pandas as pd
import seaborn as sns

from ..extra import sort_samples_by_correlation


def plot_gene_distribution(gene, exp_table, group_orders, groups):
    results = []

    for name in group_orders:
        group = [group for group in groups if group['name'] == name][0]
        try:
            results.append(exp_table.loc[gene, group['samples']].values)
        except:
            pass
            exit()

    fig = plt.figure(figsize=(12, 6))
    g = sns.boxplot(results)
    t = g.set_xticklabels(labels=group_orders, rotation=90)
    io = StringIO()
    plt.savefig(io, format='png')
    my_plot = base64.encodestring(io.getvalue())
    plt.close(fig)

    return my_plot


def gene_dist(config_file, group_and_comparisons, dataset, gene):
    groups = group_and_comparisons['group_definitions']

    summary = pd.read_csv(dataset['summary'], sep='\t')

    exp = pd.read_csv(dataset['expression_table'], sep='\t', index_col=0)

    index_order_name = sort_samples_by_correlation(group_and_comparisons)
    return plot_gene_distribution(gene, exp, index_order_name, groups)
