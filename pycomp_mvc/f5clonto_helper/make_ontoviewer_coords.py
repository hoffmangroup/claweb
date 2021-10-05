import argparse
import json
import sys

from . cytoscape_utils import get_node_attr_from_cytoscape


def main(cytoscape_file, output_graph):
    nodes, edges = get_node_attr_from_cytoscape(cytoscape_file)

    for node in nodes:
        if nodes[node]["name"] == "sac":
            nodes[node]["color"] = "orange"
            nodes[node]["type"] = "short_node"
        elif nodes[node]["name"] == "mc":
            nodes[node]["color"] = "green"
            nodes[node]["type"] = "short_node"
        else:
            if nodes[node]["name"] == "stuff accumulating cell":
                nodes[node]["color"] = "orange"
            elif nodes[node]["name"] == "motile cell":
                nodes[node]["color"] = "green"
            else:
                nodes[node]["color"] = "black"
            nodes[node]["type"] = "chart_node"

    ########## HEMAT ##########
    anchor_x, anchor_y = (0, 1350)
    x_dist, y_dist = (220, 220)
    cols = [0, x_dist * 1, x_dist * 2, x_dist * 3.2, x_dist * 4.3]
    cols = [anchor_x + c for c in cols]

    rows = [y_dist * 0, y_dist * 1, y_dist * 2, y_dist * 3,
            y_dist * 4, y_dist * 5, y_dist * 6]
    rows = [anchor_y - r for r in rows]

    nodes_coord_hemat = {
        29796: {'name': 'hematopoietic\ncell', 'x': (cols[3] - cols[0]) / 2,
                'y': rows[0] + y_dist * 0.5},

        29795: {'name': 'blood\ncell', 'x': cols[0], 'y': rows[1]},
        29800: {'name': 'granulocyte', 'x': cols[0], 'y': rows[3]},

        29833: {'name': 'myeloid\ncell', 'x': cols[1], 'y': rows[1]},
        29801: {'name': 'myeloid\nleukocyte', 'x': cols[1], 'y': rows[2]},
        29828: {'name': 'monocyte', 'x': cols[2], 'y': rows[3]},
        29835: {'name': 'CD14-positive\nmonocyte', 'x': cols[2], 'y': rows[4]},
        29850: {'name': 'classical\nmonocyte', 'x': cols[2], 'y': rows[5]},

        29782: {'name': 'mc**', 'x': cols[2] + x_dist * .2, 'y': rows[1] + y_dist * .5},
        29825: {'name': 'leukocyte', 'x': cols[2], 'y': rows[1]},
        29827: {'name': 'nongranular\nleukocyte', 'x': cols[3], 'y': rows[2]},
        29824: {'name': 'dendritic\ncell', 'x': cols[2], 'y': rows[2]},

        29849: {'name': 'phagocyte', 'x': (cols[1] - cols[0]) / 2, 'y': (rows[4] + rows[5]) / 2},
        29781: {'name': 'mc**', 'x': cols[0], 'y': rows[4] + y_dist * .2},
        29778: {'name': 'sac*', 'x': cols[1], 'y': rows[4] + y_dist * .2},
        29843: {'name': 'hematopoietic\nprecursor\ncell', 'x': cols[3], 'y': rows[1]},

        29826: {'name': 'nucleate\ncell', 'x': cols[4], 'y': rows[2]},
        29799: {'name': 'lymphocyte', 'x': cols[4], 'y': rows[3]},
        29818: {'name': 'lymphocyte\nof B lineage', 'x': cols[3], 'y': rows[4]},
        29817: {'name': 'B cell', 'x': cols[3], 'y': rows[5]},
        29798: {'name': 'T cell', 'x': cols[4], 'y': rows[4]},
        29830: {'name': 'alpha-beta\nT cell', 'x': cols[4], 'y': rows[5]},
        29829: {'name': 'CD8-positive,\nalpha-beta\nT cell', 'x': cols[4], 'y': rows[6]}, }

    ########## EPITH ##########
    anchor_x, anchor_y = (0, 2500)
    x_dist, y_dist = (235, 250)
    cols = [x_dist * 0, x_dist * 1, x_dist * 2.2, x_dist * 3.2, x_dist * 4,
            x_dist * 5, x_dist * 6, x_dist * 7, x_dist * 8, x_dist * 9]
    cols = [anchor_x + c for c in cols]

    rows = [anchor_y - 2600, y_dist * 1, y_dist * 2, y_dist * 3, y_dist * 4]
    rows = [anchor_y - r for r in rows]

    nodes_coord_epith = {

        29788: {'name': 'epithelial\ncell', 'x': (cols[1] + cols[8]) / 2, 'y': rows[0]},

        29792: {'name': 'columnar-cuboidal\nepithelial\ncell', 'x': cols[1], 'y': rows[1]},
        29811: {'name': 'neurecto-epithelial\ncell', 'x': cols[1], 'y': rows[2]},
        29810: {'name': 'melanocyte', 'x': (cols[0] + cols[1]) / 2, 'y': rows[3]},
        54910: {'name': 'sac*', 'x': cols[0], 'y': rows[1]},
        29809: {'name': 'pigment\ncell', 'x': cols[0], 'y': rows[2]},

        29832: {'name': 'ecto-epithelial\ncell', 'x': cols[2], 'y': rows[1]},
        29838: {'name': 'general\necto-epithelial\ncell', 'x': cols[2], 'y': rows[2]},

        29790: {'name': 'squamous\nepithelial\ncell', 'x': cols[3], 'y': rows[1]},
        29793: {'name': 'mesothelial\ncell', 'x': cols[3] + x_dist * .6, 'y': rows[3]},
        29789: {'name': 'blood\nvessel\nendothelial\ncell', 'x': cols[3], 'y': rows[4]},
        29794: {'name': 'lining\ncell', 'x': cols[4] + x_dist * .25, 'y': rows[2]},
        29805: {'name': 'meso-epithelial\ncell', 'x': cols[5], 'y': rows[1]},
        29804: {'name': 'endothelial\ncell', 'x': cols[5], 'y': (rows[2] + rows[3]) / 2},
        29791: {'name': 'endothelial\ncell\nof vascular\ntree', 'x': cols[5], 'y': (rows[3] + rows[4]) / 2},

        29845: {'name': 'kidney\nepithelial\ncell', 'x': cols[6], 'y': rows[1]},
        29844: {'name': 'epithelial\ncell of\nnephron', 'x': cols[6], 'y': rows[2]},

        29848: {'name': 'hepatocyte', 'x': cols[7], 'y': rows[1]},
        29797: {'name': 'epithelial\ncell\nof lung', 'x': cols[4], 'y': rows[1]},

        29836: {'name': 'endo-epithelial\ncell', 'x': cols[8], 'y': rows[1]},
        29775: {'name': 'respiratory\nepithelial\ncell', 'x': (cols[7] + cols[8]) / 2, 'y': rows[2]},
        29776: {'name': 'epithelial\ncell of\nalimentary\ncanal', 'x': (cols[8] + cols[9]) / 2, 'y': rows[2]},
    }

    ########## CONNECT ##########
    anchor_x, anchor_y = (1400, 1850)
    x_dist, y_dist = (220, 220)
    cols = [x_dist * 0, x_dist * 1, x_dist * 2, x_dist * 3, x_dist * 4]
    cols = [anchor_x + c for c in cols]

    rows = [y_dist * 0, y_dist * 1, y_dist * 2, y_dist * 3, y_dist * 4.2]
    rows = [anchor_y - r for r in rows]

    nodes_coord_connect = {
        29787: {'name': 'connective\ntissue\ncell', 'x': cols[2], 'y': rows[1]},

        29808: {'name': 'fat\ncell', 'x': cols[0], 'y': rows[2]},

        29786: {'name': 'fibroblast', 'x': cols[1], 'y': rows[2]},
        29842: {'name': 'skin\nfibroblast', 'x': cols[0], 'y': rows[3]},
        29840: {'name': 'preadipocyte', 'x': cols[1], 'y': rows[3]},

        29820: {'name': 'stromal\ncell', 'x': cols[2], 'y': rows[2]},
        29812: {'name': 'secretory\ncell', 'x': cols[3], 'y': rows[2]},
        29819: {'name': 'extracellular\nmatrix\nsecreting\ncell', 'x': cols[2], 'y': rows[3]},
        29847: {'name': 'GAG\nsecreting\ncell', 'x': cols[2], 'y': rows[4]},
        29784: {'name': 'stem\ncell', 'x': cols[4], 'y': rows[0]},
        29807: {'name': 'multi\nfate\nstem\ncell', 'x': cols[4], 'y': rows[1]},
        29806: {'name': 'mesenchymal\ncell', 'x': cols[4], 'y': rows[2]},
        29780: {'name': 'mc**', 'x': cols[3] + x_dist * .3, 'y': rows[1] - y_dist * .3},
        29777: {'name': 'sac*', 'x': cols[0], 'y': rows[1] - y_dist * .3},
    }

    ########## MUSCLE ##########
    anchor_x, anchor_y = (1300, 800)
    x_dist, y_dist = (220, 220)

    nodes_coord_muscle = {
        29815: {'name': 'electrically\nresponsive\ncell', 'x': anchor_x + x_dist * .5, 'y': anchor_y},
        29813: {'name': 'contractile\ncell', 'x': anchor_x - x_dist * .5, 'y': anchor_y},
        29814: {'name': 'muscle\ncell', 'x': anchor_x, 'y': anchor_y - y_dist * 1},
        29823: {'name': 'smooth\nmuscle\ncell', 'x': anchor_x, 'y': anchor_y - y_dist * 2},
        29822: {'name': 'vascular\nassociated\nsmooth\nmuscle\ncell', 'x': anchor_x, 'y': anchor_y - y_dist * 3.2},
    }

    ########## REST ##########
    anchor_x, anchor_y = (1600, 550)
    x_dist, y_dist = (220, 220)

    cols = [x_dist * 0, x_dist * 1, x_dist * 2, x_dist * 3]
    cols = [anchor_x + c for c in cols]

    rows = [y_dist * 0, y_dist * 1, y_dist * 2, y_dist * 3, y_dist * 4]
    rows = [anchor_y - r for r in rows]

    nodes_coord = {
        29803: {'name': 'neural\ncell', 'x': cols[0], 'y': rows[0]},
        29802: {'name': 'neuron\nassociated\ncell', 'x': cols[0], 'y': rows[1]},
        29846: {'name': 'glial\ncell', 'x': cols[0], 'y': rows[2]},
        29839: {'name': 'embryonic\ncell', 'x': cols[1], 'y': rows[0]},
        29821: {'name': 'extraembryonic\ncell', 'x': cols[1], 'y': rows[1]},
        29841: {'name': 'cardiocyte', 'x': cols[1], 'y': rows[2]},
        29785: {'name': 'non-terminally\ndifferentiated\ncell', 'x': cols[2], 'y': rows[0]},
        29831: {'name': 'supportive\ncell', 'x': cols[2], 'y': rows[1]},
        29816: {'name': 'cellof skeletal\nmuscle', 'x': cols[2], 'y': rows[2]},
        29834: {'name': 'bone\ncell', 'x': cols[3], 'y': rows[0]},
        29837: {'name': 'bone\nmarrow\ncell', 'x': cols[3], 'y': rows[1]},

    }

    ########## LEGEND ##########
    anchor_x, anchor_y = (0, 2600)
    x_dist, y_dist = (220, 200)
    nodes_coord_legend = {
        29779: {'name': '*stuff\naccumulating\ncell', 'x': anchor_x, 'y': anchor_y},
        29783: {'name': '**motile\ncell', 'x': anchor_x + x_dist, 'y': anchor_y},
    }

    nodes_coord.update(nodes_coord_epith)
    nodes_coord.update(nodes_coord_hemat)
    nodes_coord.update(nodes_coord_muscle)
    nodes_coord.update(nodes_coord_connect)
    nodes_coord.update(nodes_coord_legend)

    nodes_print_name = {
        "kidney cell;;kidney epithelial cell": "kidney\nepithelial\ncell",
        "CD14-positive, CD16-negative classical monocyte;;classical monocyte": "CD14-positive,\nCD16-negative\nclassical\nmonocyte",
        "GAG secreting cell;;carbohydrate secreting cell": "GAG\nsecreting\ncell",
        "endopolyploid cell;;hepatocyte;;metabolising cell;;polyploid cell": "hepatocyte",
        "defensive cell;;phagocyte": "phagocyte",
        "barrier cell;;lining cell": "lining\ncell",
        "non-striated muscle cell;;smooth muscle cell;;visceral muscle cell": "smooth\nmuscle\ncell",
        "glial cell;;glial cell (sensu Vertebrata)": "glial\ncell\n(sensu\nVertebrata)",
        "electrically active cell;;electrically responsive cell": "electrically\nresponsive\ncell",
        "alpha-beta T cell;;mature T cell;;mature alpha-beta T cell": "mature\nalpha-beta\nT cell",
        "multi fate stem cell;;somatic stem cell": "multi\nfate\nstem\ncell",
    }

    for node_id in nodes_coord:
        nodes[str(node_id)]["node_print_name"] = nodes_print_name.get(nodes[str(node_id)]["shared_name"],
                                                                      nodes_coord[node_id]["name"])
        nodes[str(node_id)]["y"] = nodes_coord[node_id]["y"]
        nodes[str(node_id)]["x"] = nodes_coord[node_id]["x"]

    ontoviewer_coords = {
        "nodes": nodes,
        "edges": edges
    }

    with open(output_graph, "w") as file_handler:
        json.dump(ontoviewer_coords, file_handler, indent=4)


def parse_args():
    parser = argparse.ArgumentParser(description='Make graph file with node location and edges.')
    parser.add_argument('cytoscape_file', type=str, help='path to cytoscape xgmml file.')
    parser.add_argument('output_graph', type=str, help='path to output file.')
    args = parser.parse_args(sys.argv[1:])

    return args


def cli_make_graph_coord():
    args = parse_args()
    main(args.cytoscape_file, args.output_graph)


if __name__ == "__main__":
    CYTOSCAPE_FILE = "../../data/cytoscape_cl_display_config.xgmml"
    OUTPUT_GRAPH = "../../output/ontoviewer_graph.json"

    main(CYTOSCAPE_FILE, OUTPUT_GRAPH)
