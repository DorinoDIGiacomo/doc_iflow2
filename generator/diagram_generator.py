import os
from models import interface
import textwrap

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"

from graphviz import Digraph


def generate_process_flow(interface, output_file):

    print("\n========== Diagram Generator ==========\n")

    graph = Digraph("SAP_CPI_Process", format="png")

    graph.attr(
        rankdir="TB",
        bgcolor="white",
        splines="ortho",
        nodesep="0.15",
        ranksep="0.20",
        pad="0.10",
        dpi="600",
        size="8.5,11",
        ratio="compress",
    )

    graph.attr(
        "node", fontname="Calibri", fontsize="11", style="filled,rounded", shape="box"
    )

    # =====================================================
    # Source System
    # =====================================================

    graph.node(
        "SOURCE",
        """<
    <TABLE BORDER="0" CELLBORDER="0" CELLPADDING="2">
    <TR>
    <TD ALIGN="CENTER">
        <FONT POINT-SIZE="14"><B>Source System</B></FONT><BR/>
        <FONT POINT-SIZE="10">Inbound</FONT>
    </TD>
    </TR>
</TABLE>
>""",
        fillcolor="#EAF6EA",
        color="#5B8A5B",
        penwidth="1.5",
        fontsize="15",
        margin="0.00",
    )

    # =====================================================
    # Target System
    # =====================================================

    graph.node(
        "TARGET",
        """<
<TABLE BORDER="0" CELLBORDER="0" CELLPADDING="2">

    <TR>
    <TD ALIGN="CENTER">
        <FONT POINT-SIZE="14"><B>Target System</B></FONT><BR/>
        <FONT POINT-SIZE="10">Outbound</FONT>
    </TD>
</TR>

</TABLE>
>""",
        fillcolor="#FCECEC",
        color="#B85450",
        penwidth="1.5",
        fontsize="15",
        margin="0.00",
    )

    # =====================================================
    # SAP Integration Suite Cluster
    # =====================================================

    with graph.subgraph(name="cluster_integration") as c:

        c.attr(
            label="""<
<TABLE BORDER="0" CELLBORDER="0" CELLPADDING="2">

    <TR>
        <TD ALIGN="CENTER">
            <FONT POINT-SIZE="18">
                <B>SAP Integration Suite</B>
            </FONT>
        </TD>
    </TR>

    <TR>
        <TD ALIGN="CENTER">
            <FONT POINT-SIZE="12">
                Cloud Integration
            </FONT>
        </TD>
    </TR>

</TABLE>
>""",
            labelloc="t",
            labeljust="c",
            style="filled",
            fillcolor="#FBFDFF",
            color="#8FAADC",
            penwidth="1.2",
            fontname="Calibri",
            fontsize="18",
            margin="6",
        )

        c.attr(rankdir="TB")

        if hasattr(interface, "process_steps") and interface.process_steps:

            for index, step in enumerate(interface.process_steps, start=1):

                if isinstance(step, dict):
                    title = step.get("title", f"Step {index}")
                    overview = step.get("description", "")
                else:
                    title = getattr(step, "title", f"Step {index}")
                    overview = getattr(step, "description", "")

                # Keep overview short
                if overview:
                    overview = overview.replace("<", "").replace(">", "")
                    overview = "<BR ALIGN='CENTER'/>".join(
                        textwrap.wrap(
                            overview,
                            width=50,
                            break_long_words=False,
                            break_on_hyphens=False,
                        )
                    )

                    label = f"""<
<TABLE BORDER="0"
       CELLBORDER="0"
       CELLPADDING="2"
       CELLSPACING="0"
       WIDTH="370">

    <TR>
        <TD ALIGN="CENTER" BALIGN="CENTER" VALIGN="MIDDLE">
            <FONT POINT-SIZE="14">
                <B>{index}. {title}</B>
            </FONT>
        </TD>
    </TR>

    <TR>
        <TD ALIGN="CENTER" BALIGN="CENTER" VALIGN="MIDDLE">
            <FONT POINT-SIZE="12">
                {overview}
            </FONT>
        </TD>
    </TR>

</TABLE>
>"""
                else:
                    label = f"""<
<TABLE BORDER="0"
       CELLBORDER="0"
       CELLPADDING="2"
       CELLSPACING="0"
       WIDTH="370">

    <TR>
        <TD ALIGN="CENTER" BALIGN="CENTER" VALIGN="MIDDLE">
            <FONT POINT-SIZE="15">
                <B>{index}. {title}</B>
            </FONT>
        </TD>
    </TR>

</TABLE>
>"""

                c.node(
                    f"STEP_{index}",
                    label,
                    fillcolor="#F8FBFF",
                    color="#7FA6D9",
                    penwidth="1.4",
                    margin="0.00",
                )

                if index > 1:
                    c.edge(
                        f"STEP_{index-1}",
                        f"STEP_{index}",
                        color="#6C8EBF",
                        penwidth="1.4",
                        arrowsize="0.9",
                    )

    # =====================================================
    # Connect Source -> Flow -> Target
    # =====================================================

    if hasattr(interface, "process_steps") and interface.process_steps:

        graph.edge(
            "SOURCE",
            "STEP_1",
            minlen="1",
            color="#6C8EBF",
            penwidth="1.4",
            arrowsize="0.9",
        )

        graph.edge(
            f"STEP_{len(interface.process_steps)}",
            "TARGET",
            minlen="1",
            color="#6C8EBF",
            penwidth="1.4",
            arrowsize="0.9",
        )

    graph.render(output_file, cleanup=True)

    print(f"Diagram generated : {output_file}.png")
