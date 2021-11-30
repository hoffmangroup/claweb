import pandas as pd


def get_number_of_cell_types_with_results(cfg):
    n_cell_types_list = []
    for dataset in cfg['datasets']:
        df = pd.read_csv(dataset['summary'], sep='\t')
        n_cell_types = pd.concat([df.cl1, df.cl2]).unique().size
        n_cell_types_list.append(n_cell_types)

    return max(n_cell_types_list)
