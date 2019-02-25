import sys
import os
import shutil
import argparse

import pandas as pd

from pycomp_mvc import extra
from pycomp_mvc.controller import genes
from pycomp_mvc.controller import groups
from pycomp_mvc.controller import index
from pycomp_mvc.controller.comparisons import comparison_list
from pycomp_mvc.controller.comparisons import comparisons


def main(args):
    cfg, gac = extra.load_configs(args.config, args.group_and_comparison)

    # create website base directory
    if not os.path.exists(cfg['website']['output']):
        os.makedirs(cfg['website']['output'])

    # copy JS and CSS files to the website base directory
    this_path = os.path.dirname(os.path.realpath(__file__))

    static_path = os.path.join(this_path, 'pycomp_mvc', 'static')
    static_output_path = os.path.join(cfg['website']['output'], 'static')

    if not os.path.exists(static_output_path):
        shutil.copytree(static_path, static_output_path)

    # create index.html
    index.main(cfg)

    # create subsection main pages
    comparison_list.comparison_list(cfg, gac)
    genes.gene_list(cfg, gac)
    groups.group_list(cfg, gac)

    # create individual web pages
    for group in gac['group_definitions']:
        groups.group(cfg, gac, group['id'])

    for dataset in cfg['datasets']:
        df = pd.read_csv(dataset['summary'], sep='\t')
        df = df[(df.robustness == 10) & (df.accuracy > .9)]

        for gene in set(df.gene.tolist()):
            genes.gene_card(cfg, gac, dataset, gene)

    for comp in gac['comparisons']:
        comparisons.comparisons(cfg, gac, comp['id'])


def parse_args(args):
    parser = argparse.ArgumentParser(description='Make website')
    parser.add_argument('config', type=str, help='path to config file')
    parser.add_argument('group_and_comparison', type=str, help='path to group and comparison file')

    return parser.parse_args(args)


if __name__ == '__main__':
    # args = sys.argv[1:]
    args = [
        '/biga/01_TF_RRF_500/global_config.yaml',
        '/biga/01_TF_RRF_500/f5_group_and_comparisons.yaml']

    main(parse_args(args))
