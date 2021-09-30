import xml.dom.minidom as minidom


def get_node_attr_from_cytoscape(xgmml_filename):
    """Get node attributes name, id, shared_name, x, y, w, id, and edges from
    an xgmml file from cytoscape.

    Return nodes and edges"""

    assert "xgmml" in xgmml_filename

    doc = minidom.parse(xgmml_filename)

    nodes = {}
    for node in doc.getElementsByTagName("node"):
        for att in node.getElementsByTagName("att"):
            if att.getAttribute("name") == "shared name":
                shared_name = att.getAttribute("value")
                graphic = node.getElementsByTagName("graphics")
                if graphic:
                    graphic = graphic[0]
                else:
                    continue
                att = {
                    "name": node.getAttribute("label"),
                    "id": node.getAttribute("id"),
                    "shared_name": shared_name,
                    "x": float(graphic.getAttribute("x")),
                    # in cytoscape y are negative at the top and positive at the bottom,
                    # it's the opposite in matplotlib so we multiply by -1
                    "y": -float(graphic.getAttribute("y")),
                }
                nodes[node.getAttribute("id")] = att

    # transform coord to remove negative values
    min_x = min(v["x"] for v in nodes.values())
    min_y = min(v["y"] for v in nodes.values())

    for node in nodes:
        nodes[node]["x"] = nodes[node]["x"] + abs(min_x)
        nodes[node]["y"] = nodes[node]["y"] + abs(min_y)

    edges = {}
    for edge in doc.getElementsByTagName("edge"):
        source = edge.getAttribute("source")
        target = edge.getAttribute("target")

        if not all(e in nodes for e in [source, target]):
            continue
        att = {"source": source, "target": target}
        edges[edge.getAttribute("id")] = att

    return nodes, edges
