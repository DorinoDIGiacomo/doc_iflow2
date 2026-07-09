import os

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"

from graphviz import Digraph


def generate_process_flow(interface, output_file):

    print("\n========== Diagram Generator ==========\n")

    graph = Digraph(
        "SAP_CPI_Process",
        format="png"
    )

    graph.attr(
        rankdir="LR",
        splines="ortho",
        nodesep="0.5",
        ranksep="1.0",
        dpi="200"
    )

    graph.attr("node",
               fontname="Arial",
               fontsize="10",
               style="filled,rounded",
               shape="box")

    # ------------------------
    # Create Nodes
    # ------------------------

    for component in interface.components:

        color = "#FFFFFF"
        shape = "box"

        t = component.category.lower()

        if "start" in t:
            color = "#A8E6A3"
            shape = "circle"

        elif "end" in t:
            color = "#FFB3B3"
            shape = "doublecircle"

        elif "request reply" in t:
            color = "#AED6F1"

        elif "content modifier" in t:
            color = "#F9E79F"

        elif "mapping" in t:
            color = "#D2B4DE"

        elif "splitter" in t:
            color = "#F5CBA7"

        elif "groovy" in t:
            color = "#D5DBDB"

        elif "converter" in t:
            color = "#FADBD8"

        graph.node(
            component.id,
            f"{component.category}\n{component.name}",
            shape=shape,
            fillcolor=color
        )

    # ------------------------
    # Connections
    # ------------------------

    for connection in interface.connections:

        graph.edge(
            connection.source,
            connection.target
        )

    graph.render(
        output_file,
        cleanup=True
    )

    print(f"Diagram generated : {output_file}.png")