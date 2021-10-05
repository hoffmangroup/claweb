import os
import sys
import argparse
import pandas as pd
import json

from .. extra import GAC

from collections import defaultdict


def get_up_down_count(df):
    # add up and down count
    res = defaultdict(
        lambda: {"up": 0, "down": 0})

    for i, row in df.iterrows():
        if row["t-test"] > 0:
            up_in = row["cl1"]
            down_in = row["cl2"]
        else:
            up_in = row["cl2"]
            down_in = row["cl1"]

        res[(row.gene, up_in)]["up"] += 1
        res[(row.gene, down_in)]["down"] += 1
    return res


def main(gac_filepath, summary_filepath, dataset_name, rob=10, acc=.9, outdir='.'):
    # load GAC config file
    gac = GAC(gac_filepath)

    # load summary dataset
    df = pd.read_csv(summary_filepath, sep="\t")
    df = df[(df.robustness == rob) & (df.accuracy > acc)]

    # get dict[(gene, cl_id)] -> {"up": x, "down": y}
    up_down_dict = get_up_down_count(df)

    # add neither count by subtracting up + down to number of comparison
    for k, v in up_down_dict.items():
        n_comp = gac.get_n_comp_from_id(k[1])
        up_down_dict[k]['neither'] = n_comp - (v['up'] + v['down'])

    # convert cl_id to cl_name and unstack the dict keys:
    # up_down_dict[(gene, cl_id)]: up_down_count -> res[gene][cl_name]: up_down_count
    res = defaultdict(lambda: dict())
    for (gene, cl_id), up_down_count in up_down_dict.items():
        cl_name = gac.get_name_from_group_id(cl_id)
        res[gene][cl_name] = up_down_count

    # save res as json
    outfile_id = f"{dataset_name}_rob{rob}acc{acc * 100}"

    with open(f"{outdir}/up_down_neither_counts_{outfile_id}.json", "w") as outfile:
        json.dump(dict(res), outfile)


def parse_args():
    parser = argparse.ArgumentParser(description='Collect lineage scores for each gene.')
    parser.add_argument('gac_filepath', type=str,
                        help='path to the yaml file with group and comparison definitions.')
    parser.add_argument('summary_filepath', type=str, help='path to the summary file.')
    parser.add_argument('--dataset_name', type=str, help='prefix of the output filename. '
                                                         'By default, it is what precede the pattern "_summary" '
                                                         'from `summary_filepath`.')
    parser.add_argument('--rob', type=int, default=10, help="robustness threshold (int).")
    parser.add_argument('--acc', type=float, default=.9, help="accuracy threshold (float).")
    parser.add_argument('--outdir', type=str, default=os.getcwd(), help="path to the output directory.")

    args = parser.parse_args(sys.argv[1:])
    if args.dataset_name is None:
        args.dataset_name = os.path.basename(os.path.splitext(args.summary_filepath)[0])

    return args


def cli_make_updown_count():
    args = parse_args()
    main(args.gac_filepath, args.summary_filepath,
         args.dataset_name, args.rob, args.acc, args.outdir)


if __name__ == "__main__":
    cli_make_updown_count()
