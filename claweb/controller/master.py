#!/usr/bin/env python
import argparse
import multiprocessing
import os
import shutil
import sys
from functools import partial

import pandas as pd

from . import genes
from . import groups
from . import index
from .comparisons import comparison_list
from .comparisons import comparisons
from .. import extra


def make_index(cfg):
    cfg = extra.load_config(cfg)

    # create website base directory
    if not os.path.exists(cfg['website']['output']):
        os.makedirs(cfg['website']['output'])

    # copy JS and CSS files to the website base directory
    pycomp_module_path = os.path.dirname(extra.__file__)

    static_path = os.path.join(pycomp_module_path, 'static')
    static_output_path = os.path.join(cfg['website']['output'], 'static')

    if not os.path.exists(static_output_path):
        shutil.copytree(static_path, static_output_path)

    # create index.html
    index.main(cfg)


def make_genecards(cfg, gac, n_thread):
    cfg = extra.load_config(cfg)
    gac = extra.load_gac(gac)

    make_index(cfg)
    genes.gene_list(cfg, gac)
    for dataset in cfg['datasets']:
        df = pd.read_csv(dataset['summary'], sep='\t')
        df = df[(df.robustness == 10) & (df.accuracy > .9)]

        pool = multiprocessing.Pool(n_thread)
        make_gene_card = partial(genes.gene_card, cfg, gac, dataset)
        gene_list = set(df.gene.tolist())
        pool.map(make_gene_card, gene_list)


def make_groups(cfg, gac, n_thread):
    cfg = extra.load_config(cfg)
    gac = extra.load_gac(gac)

    make_index(cfg)
    groups.group_list(cfg, gac)

    pool = multiprocessing.Pool(n_thread)
    make_group = partial(groups.group, cfg, gac)
    group_ids = [group['id'] for group in gac['group_definitions']]
    pool.map(make_group, group_ids)


def make_comparisons(cfg, gac, n_thread):
    cfg = extra.load_config(cfg)
    gac = extra.load_gac(gac)

    make_index(cfg)
    comparison_list.comparison_list(cfg, gac)

    pool = multiprocessing.Pool(n_thread)
    make_comparison = partial(comparisons.comparisons, cfg, gac)
    comparison_ids = [comp['id'] for comp in gac['comparisons']]
    pool.map(make_comparison, comparison_ids)


def main(config, group_and_comparison, n_thread):
    cfg, gac = extra.load_configs(config, group_and_comparison)

    make_index(cfg)
    make_genecards(cfg, gac, n_thread)
    make_groups(cfg, gac, n_thread)
    make_comparisons(cfg, gac, n_thread)


def parse_args(args):
    parser = argparse.ArgumentParser(description='Make website')
    parser.add_argument('config', type=str, help='path to config file.')
    parser.add_argument('group_and_comparison', type=str, help='path to group and comparison file.')
    parser.add_argument('--n_thread', type=int, default=1, help='make genecards with `n` thread.')
    args = parser.parse_args(args)

    args.n_thread = min(os.cpu_count(), args.n_thread)

    return args


def cli_make_website(args=sys.argv[1:]):
    args = parse_args(args)
    main(args.config, args.group_and_comparison, args.n_thread)


def cli_make_comparisons(args=sys.argv[1:]):
    args = parse_args(args)
    make_comparisons(args.config, args.group_and_comparison, args.n_thread)


def cli_make_genes(args=sys.argv[1:]):
    args = parse_args(args)
    make_genecards(args.config, args.group_and_comparison, args.n_thread)


if __name__ == '__main__':
    # cli_make_website()
    pass
