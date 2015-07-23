__author__ = 'mickael'

from pycomp_mvc.model.comparisons import comparison

__author__ = 'mickael'

from pycomp_mvc import extra
from pycomp_mvc.controller import index
# from pycomp_mvc.controller.comparisons import comparisons

if __name__ == '__main__':
    cfg, gac = extra.load_configs('/home/mickael/Projects/pycomp_mvc_test/input/global_config_ac2.yaml',
                                  '/home/mickael/Projects/pycomp_mvc_test/input/2015-04-02_f5_primary-cell_CL_comparisons_libid.yml')

    # comparison_list.comparison_list(cfg, gac)
    index.main(cfg)