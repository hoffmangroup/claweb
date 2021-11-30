__author__ = 'mickael'

import argparse
import yaml
import sys


def run(config_file, comp_file):

    with open(config_file) as yaml_file:
        cfg = yaml.load(yaml_file)

    with open(comp_file) as yaml_file:
        group_and_comparisons = yaml.load(yaml_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Regularized Random Forest.')
    parser.add_argument('--config_file', type=str, help='full path to the config file', required=True)
    parser.add_argument('--comp_file', type=str, help='full path to the comparison file', required=True)

    args = parser.parse_args(sys.argv[1:])

    run(args.config_file, args.comp_file)

#TODO: handle the website folder creation