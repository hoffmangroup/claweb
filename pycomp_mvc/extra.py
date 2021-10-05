__author__ = 'mickael'

import os
import yaml


def load_config(config_path):
    assert isinstance(config_path, str) or isinstance(config_path, dict)

    if isinstance(config_path, str):
        with open(config_path) as yaml_file:
            cfg = yaml.safe_load(yaml_file)
    else:
        cfg = config_path

    assert 'datasets' in cfg

    if 'basedir' not in cfg:
        cfg['basedir'] = os.getcwd()
    elif cfg['basedir'] == 'config':
        cfg['basedir'] = os.path.dirname(config_path)

    for dataset in cfg['datasets']:
        assert 'name' in dataset
        assert 'n_tree' in dataset

        if 'output' not in dataset:
            output = '{}_{}'.format(dataset['name'], dataset['n_tree'])
            dataset['output'] = os.path.join(cfg['basedir'], output)

        if 'summary' not in dataset:
            summary = '{}_summary.tsv'.format(dataset['output'])
            dataset['summary'] = os.path.join(cfg['basedir'], summary)

    if 'website' not in cfg:
        cfg['website'] = dict()
        cfg['website']['output'] = os.path.join(cfg['basedir'], 'website')
        cfg['website']['url'] = '.'

    return cfg


def load_gac(gac_file):
    assert isinstance(gac_file, str) or isinstance(gac_file, dict)

    if isinstance(gac_file, str):
        with open(gac_file) as yaml_file:
            gac = yaml.safe_load(yaml_file)
    else:
        gac = gac_file

    assert 'comparisons' in gac
    assert 'group_definitions' in gac

    return gac


def load_configs(config_file, group_and_comparisons):
    cfg = load_config(config_file)
    group_and_comparisons = load_gac(group_and_comparisons)

    return cfg, group_and_comparisons


def get_dict_from_list_dict(l, key, value):
    for d in l:
        if d[key] == value:
            return d
    return None


class GAC:
    """Group And Comparison"""

    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    @property
    def comps(self):
        return self.config["comparisons"]

    @property
    def groups(self):
        return self.config["group_definitions"]

    def get_dict_from_id(self, l, _id):
        return get_dict_from_list_dict(l, "id", _id)

    def get_comp_from_id(self, _id):
        return self.get_dict_from_id(self.comps, _id)

    def get_group_from_id(self, _id):
        return self.get_dict_from_id(self.groups, _id)

    def get_samples_from_group_id(self, _id):
        group = self.get_group_from_id(_id)
        return group["samples"]

    def get_name_from_group_id(self, _id):
        return self.get_group_from_id(_id)["name"]

    def get_group_from_name(self, name):
        return get_dict_from_list_dict(self.groups, "name", name)

    def get_n_comp_from_id(self, _id):
        comparisons = [None
                       for d in self.comps
                       if _id in d.values()]
        return len(comparisons)


# import numpy as np
# import pandas as pd
# from scipy.cluster.hierarchy import linkage, leaves_list

# def sort_samples_by_correlation(group_and_comparisons):
#
#     groups = group_and_comparisons['group_definitions']
#
#     samples_list = [group['samples'] for group in groups]
#     samples_flatten = [e for samples in samples_list for e in samples]
#     samples_index = pd.Index(set(samples_flatten))
#
#     m = [[1 if samples in group['samples'] else 0 for samples in samples_index] for group in groups]
#     m_t = np.transpose(m)
#
#     columns = [group['name'] for group in groups]
#
#     sample_cl_df = pd.DataFrame(m_t, columns=columns, index=samples_index)
#     term_correlation = sample_cl_df.corr()
#
#     ln = linkage(term_correlation)
#     index_oder = leaves_list(ln)
#
#     return term_correlation.iloc[:, index_oder].columns
