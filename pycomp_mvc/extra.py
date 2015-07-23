__author__ = 'mickael'


import yaml


def load_configs(config_file, group_and_comparisons):
    with open(config_file) as yaml_file:
        cgf = yaml.load(yaml_file)

    with open(group_and_comparisons) as yaml_file:
        group_and_comparisons = yaml.load(yaml_file)

    return cgf, group_and_comparisons


