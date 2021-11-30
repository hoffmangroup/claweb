#!/usr/bin/env python

import sys
import os
import shutil
import argparse

import pandas as pd

from claweb import extra
from claweb.controller import genes
from claweb.controller import groups
from claweb.controller import index
from claweb.controller.comparisons import comparison_list
from claweb.controller.comparisons import comparisons


def main(args):
    cfg, gac = extra.load_configs(args.config, args.group_and_comparison)

    # create website base directory
    if not os.path.exists(cfg['website']['output']):
        os.makedirs(cfg['website']['output'])

    # copy JS and CSS files to the website base directory
    pycomp_module_path = os.path.dirname(extra.__file__)

    static_path = os.path.join(pycomp_module_path, 'static')
    static_output_path = os.path.join(cfg['website']['output'], 'static')

    if os.path.exists(static_output_path):
        shutil.rmtree(static_output_path)
    shutil.copytree(static_path, static_output_path)

    # create index.html
    # index.main(cfg)
    #
    # # create subsection main pages
    # comparison_list.comparison_list(cfg, gac)
    # genes.gene_list(cfg, gac)
    # groups.group_list(cfg, gac)

    # create individual web pages
    # for group in gac['group_definitions']:
    #     groups.group(cfg, gac, group['id'])

    for dataset in cfg['datasets']:
    # for dataset in cfg['datasets'][1:2]:
        df = pd.read_csv(dataset['summary'], sep='\t')
        df = df[(df.robustness == 10) & (df.accuracy > .9)]

        assert args.gene in df.gene.unique()
        # for gene in set(df.gene.tolist()):
        genes.gene_card(cfg, gac, dataset, args.gene)


def parse_args(args):
    parser = argparse.ArgumentParser(description='Make website')
    parser.add_argument('config', type=str, help='path to config file')
    parser.add_argument('group_and_comparison', type=str, help='path to group and comparison file')
    parser.add_argument('gene', type=str, help='Generate gene card for specified gene')

    return parser.parse_args(args)


if __name__ == '__main__':
    args = sys.argv[1:]
    parse_args(args)
    # print("hello")
    main(parse_args(args))
