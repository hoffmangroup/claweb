__author__ = 'mickael'


import yaml
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, leaves_list


def load_config(config_path):
    with open(config_path) as yaml_file:
        cfg = yaml.safe_load(yaml_file)

    assert 'datasets' in cfg

    for dataset in cfg['datasets']:
        assert 'name' in dataset
        assert 'n_tree' in dataset

        if 'output' not in dataset:
            dataset['output'] = '{}_{}'.format(
                dataset['name'], dataset['n_tree'])

        if 'summary' not in dataset:
            dataset['summary'] = '{}_summary.tsv'.format(
                dataset['output'])

    return cfg


def load_configs(config_file, group_and_comparisons):
    cfg = load_config(config_file)

    with open(group_and_comparisons) as yaml_file:
        group_and_comparisons = yaml.load(yaml_file)

    return cfg, group_and_comparisons


def sort_samples_by_correlation(group_and_comparisons):

    groups = group_and_comparisons['group_definitions']

    samples_list = [group['samples'] for group in groups]
    samples_flatten = [e for samples in samples_list for e in samples]
    samples_index = pd.Index(set(samples_flatten))

    m = [[1 if samples in group['samples'] else 0 for samples in samples_index] for group in groups]
    m_t = np.transpose(m)

    columns = [group['name'] for group in groups]

    sample_cl_df = pd.DataFrame(m_t, columns=columns, index=samples_index)
    term_correlation = sample_cl_df.corr()

    ln = linkage(term_correlation)
    index_oder = leaves_list(ln)

    return term_correlation.iloc[:, index_oder].columns

