import argparse
import json
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use(backend="Agg")

FONT_SIZE = 15


def plot_node(node, t_bbox, graph_w_display, graph_h_display, ax, fig, pad=2):
    # get graph coordinates
    graph_x_display = t_bbox.p0[0] + (t_bbox.width - graph_w_display) / 2  # x0 + margin
    graph_y_display = t_bbox.p0[1] - graph_h_display
    graph_x1_display, graph_y1_display = (graph_x_display + graph_w_display, t_bbox.p0[1])
    graph_x_fig, graph_y_fig = fig.transFigure.inverted().transform((graph_x_display, graph_y_display))
    graph_w_fig, graph_h_fig = fig.transFigure.inverted().transform((graph_w_display, graph_h_display))

    # plot graph
    ax1 = fig.add_axes([graph_x_fig, graph_y_fig, graph_w_fig, graph_h_fig])
    up, down, other = (node["up"], node["down"], node["neither"])

    ax1.barh([1], [up], color="#fb9a99", edgecolor="whitesmoke")
    ax1.barh([1], [down], left=[up], color="#a6cee3", edgecolor="whitesmoke")
    ax1.barh([1], [other], left=[up + down], color="lightgray", edgecolor="whitesmoke")
    ax1.set_xlim(-0.05, 1.05)
    ax1.set_ylim(0.45, 1.55)
    ax1.set_yticks([])
    ax1.set_xticks([])
    ax1.axis("off")

    # plot contour of text and graph
    major_x_data, major_y_data = ax.transData.inverted().transform(
        (min(t_bbox.p0[0], graph_x_display), t_bbox.p0[1] - graph_h_display))
    major_x1_data, major_y1_data = ax.transData.inverted().transform(
        (max(t_bbox.p1[0], graph_x1_display), t_bbox.p1[1]))
    major_w_data = major_x1_data - major_x_data
    major_h_data = major_y1_data - major_y_data

    rect = FancyBboxPatch((major_x_data - 1, major_y_data - 1), major_w_data + pad, major_h_data + pad, linewidth=1,
                          edgecolor=node["color"], facecolor='none', boxstyle="round,pad=10")
    p = ax.add_patch(rect)

    return p


def add_up_down_count_to_nodes(nodes, up_down_df):
    """Add up, down and other counts to each nodes.
    Modify `nodes` in place"""

    columns = ["up", "down", "neither"]

    for node in nodes.values():
        if not node["type"] == "chart_node":
            continue

        node_name = node["shared_name"]

        # if "classical" in node_name:
        #     print(node_name)
        if node_name in up_down_df.index:
            values = up_down_df.loc[node_name, columns]
            values = values / values.sum()
            values = values.tolist()
        else:
            values = (0., 0., 1.)

        for tag, val in zip(columns, values):
            nodes[node["id"]][tag] = val


def main(graph_filename, up_down_filename, gene="SPI1", outfile="ontoviewer_plot.pdf", percent_up_down_threshold=0):

    with open(up_down_filename) as fh:
        up_down_dict = json.load(fh)

    with open(graph_filename) as fh:
        graph = json.load(fh)
        nodes, edges = (graph["nodes"], graph["edges"])

    up_down_df = pd.DataFrame.from_dict(up_down_dict[gene]).T

    up_down_percent = up_down_df[["up", "down"]].sum(1) / up_down_df.sum(1) * 100
    if (up_down_percent > percent_up_down_threshold).sum() == 0:
        return None

    add_up_down_count_to_nodes(nodes, up_down_df)

    fig, ax = plt.subplots(figsize=(35, 25))

    ax.set_ylim(-100, 2700)
    ax.set_xlim(-150, 2500)

    node_to_text_display = {}
    node_to_patch = {}
    node_to_patch_center = {}

    chart_nodes = {n_id: n
                   for n_id, n in nodes.items()
                   if n["type"] == "chart_node"}

    short_nodes = {n_id: n
                   for n_id, n in nodes.items()
                   if n["type"] == "short_node"}

    for node_id, node in chart_nodes.items():

        t = ax.text(node["x"], node["y"], node["node_print_name"],
                    ha="center", va="center", fontsize=FONT_SIZE)

        renderer = fig.canvas.get_renderer()

        # get display coord of the text (bbox not included)
        bbox_text = t.get_window_extent(renderer=renderer)
        node_to_text_display[node_id] = bbox_text

    wideleast_display = min([node.width for node in node_to_text_display.values()])

    mean_height_display = np.mean([node.height for node in node_to_text_display.values()])
    mean_height_display *= .7  # TODO: why this number? make height smaller

    # plot chart nodes
    for node_id, node in chart_nodes.items():
        p = plot_node(node, node_to_text_display[node_id],
                      wideleast_display + 40, mean_height_display, ax, fig)
        node_to_patch[node_id] = p

        patch_center = {
            "x": p.get_x() + p.get_width() / 2,
            "y": p.get_y() + p.get_height() / 2}
        node_to_patch_center[node_id] = patch_center

    # plot short nodes (sac and mc)
    for node_id, node in short_nodes.items():
        node_to_patch_center[node_id] = {"x": node["x"], "y": node["y"]}
        bbox = dict(facecolor='none', edgecolor=node["color"], alpha=1, boxstyle="round,pad=.3")
        t = ax.text(node["x"], node["y"], node["node_print_name"], ha="center", va="center", fontsize=FONT_SIZE, bbox=bbox)
        node_to_patch[node_id] = t

    # plot edges
    for edge_id, edge in edges.items():
        u, v = (edge["target"], edge["source"])
        pos_u, pos_v = (node_to_patch_center[u], node_to_patch_center[v])
        arrow_coord = (pos_u["x"], pos_u["y"], pos_v["x"], pos_v["y"])
        ux, uy, vx, vy = arrow_coord
        ax.annotate("", (vx, vy), xytext=(ux, uy), arrowprops=dict(
            facecolor='black', patchA=node_to_patch[u], patchB=node_to_patch[v],
            shrinkA=.1, shrinkB=20, lw=.01, ec="black", headwidth=5, headlength=6, width=.5))
    ax.axis("off")

    # outname = "cl_spi1_newline_script"  # TODO: make parameter
    # exts = ["png", "pdf", "svg"]
    # exts = ["pdf"]
    # exts = ["png"]
    # for ext in exts:
    #     fig.savefig(f"{outname}.{ext}", bbox_inches='tight')
    fig.savefig(outfile, bbox_inches='tight')
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot a graph with lineage scores in nodes.')
    parser.add_argument('graph_json', type=str,
                        help='path to the graph description in json format.')
    parser.add_argument('lineage_scores', type=str, help='path to the file containing lineage scores.')
    parser.add_argument('gene', type=str, help='plot the lineage scores of `gene`. '
                                               'The gene should be in the lineage score file.')
    parser.add_argument('--outfile_name', type=str, help="path to the output directory.")

    args = parser.parse_args(sys.argv[1:])

    if args.outfile_name is None:
        args.outfile_name = f"{args.gene}.pdf"

    main(args.graph_json, args.lineage_scores, args.gene, args.outfile_name)
