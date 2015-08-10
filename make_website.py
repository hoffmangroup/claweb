__author__ = 'mickael'

from pycomp_mvc.model.comparisons import comparison

__author__ = 'mickael'

from pycomp_mvc import extra

from pycomp_mvc.controller import index

from pycomp_mvc.controller import groups
from pycomp_mvc.controller import genes

from pycomp_mvc.controller.comparisons import comparison_list
from pycomp_mvc.controller.comparisons import comparisons

import pandas as pd

if __name__ == '__main__':
    cfg, gac = extra.load_configs('/home/mickael/Projects/pycomp_mvc_test/input/global_config_ac2.yaml',
                                  '/home/mickael/Projects/pycomp_mvc_test/input/2015-04-02_f5_primary-cell_CL_comparisons_libid.yml')

    index.main(cfg)

    comparison_list.comparison_list(cfg, gac)
    genes.gene_list(cfg, gac)
    groups.group_list(cfg, gac)

    for group in gac['group_definitions']:
        groups.group(cfg, gac, group['id'])

    for dataset in cfg['datasets']:

        df = pd.read_csv(dataset['summary'], sep='\t')
        df = df[(df.robustness == 10) & (df.accuracy > .9)]

        for gene in set(df.gene.tolist()):
            genes.gene_card(cfg, gac, dataset, gene)

    # comparison_list.comparison_list(cfg, gac)
    for comp in gac['comparisons']:
        comparisons.comparisons(cfg, gac, comp['id'])
