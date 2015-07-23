
__author__ = 'mickael'

from pycomp_mvc import extra
from pycomp_mvc.controller import groups

import pandas as pd

if __name__ == '__main__':
    cfg, gac = extra.load_configs('/home/mickael/Projects/pycomp_mvc_test/input/global_config_ac2.yaml',
                                  '/home/mickael/Projects/pycomp_mvc_test/input/2015-04-02_f5_primary-cell_CL_comparisons_libid.yml')

    groups.group(cfg, gac, 'CL:0002076')
    groups.group_list(cfg, gac)
    # lncRNA_intergenic_antisense
    # for dataset in cfg['datasets']:
    #
    #     df = pd.read_csv(dataset['summary'], sep='\t')
    #     df = df[(df.robustness == 10) & (df.accuracy > .9)]
    #
    #     for gene in set(df.gene.tolist()):
    #         genes.gene_card(cfg, gac, dataset, gene)
    #
    # genes.gene_list(cfg, gac)