import os
import textwrap
from models import interface
from graphviz import Digraph
from generator.process_description_formatter import create_process_summary

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"

def shorten_description(text, max_words=18):
    """
    Shortens a paragraph for use inside the process flow diagram.
    """

    if not text:
        return ""

    # Remove line breaks
    text = text.replace("\n", " ").strip()

    words = text.split()

    if len(words) <= max_words:
        return text

    return " ".join(words[:max_words]) + "..."

def _generate_single_process_flow(interface, output_file, steps, first_page=False, last_page=False):

    print("\n========== Diagram Generator ==========\n")

    graph = Digraph("SAP_CPI_Process", format="png")

    graph.attr(
        rankdir="TB",
        bgcolor="white",
        splines="ortho",
        nodesep="0.05",
        ranksep="0.08",
        pad="0.03",
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

        if steps:

            for local_index, step in enumerate(steps, start=1):

                if isinstance(step, dict):
                    global_index = step.get("step_number", local_index)

                    title = step.get("title", f"Step {global_index}")
                    overview = step.get("description", "")
                else:
                    title = getattr(step, "title", f"Step {global_index}")
                    overview = getattr(step, "description", "")

                # Convert long description into diagram bullet points
                if overview:

                    bullets = create_process_summary(overview)

                    overview = ""

                    for bullet in bullets:
                        bullet = bullet.replace("<", "").replace(">", "")
                        overview += f"• {bullet}<BR ALIGN='LEFT'/>"

                    overview = overview.rstrip("<BR ALIGN='LEFT'/>")

                    label = f"""<
<TABLE BORDER="0"
       CELLBORDER="0"
       CELLPADDING="0"
       CELLSPACING="0"
       WIDTH="320">

    <TR>
        <TD ALIGN="CENTER" BALIGN="CENTER" VALIGN="MIDDLE" CELLPADDING="1">
            <FONT POINT-SIZE="13">
                <B>{global_index}. {title}</B>
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
                <B>{global_index}. {title}</B>
            </FONT>
        </TD>
    </TR>

</TABLE>
>"""

                c.node(
                    f"STEP_{local_index}",
                    label,
                    fillcolor="#F8FBFF",
                    color="#7FA6D9",
                    penwidth="1.4",
                    margin="0.02",
                )

                if local_index > 1:
                    c.edge(
                        f"STEP_{local_index-1}",
                        f"STEP_{local_index}",
                        color="#6C8EBF",
                        penwidth="1.4",
                        arrowsize="0.9",
                    )

    # =====================================================
    # Connect Source -> Flow -> Target
    # =====================================================

    if steps:

        if first_page:

            graph.edge(
                "SOURCE",
                "STEP_1",
                minlen="1",
                color="#6C8EBF",
                penwidth="1.4",
                arrowsize="0.9",
            )

        if last_page:

            graph.edge(
                f"STEP_{len(steps)}",
                "TARGET",
                minlen="1",
                color="#6C8EBF",
                penwidth="1.4",
                arrowsize="0.9",
            )

    graph.render(output_file, cleanup=True)

    print(f"Diagram generated : {output_file}.png")

def generate_process_flow(interface, output_file):
    """
    Generates a single process flow diagram containing all process steps.
    """

    if not hasattr(interface, "process_steps") or not interface.process_steps:
        return

    all_steps = []

    for i, step in enumerate(interface.process_steps, start=1):

        if isinstance(step, dict):
            step["step_number"] = i
            all_steps.append(step)

        else:
            all_steps.append({
                "step_number": i,
                "title": getattr(step, "title", f"Step {i}"),
                "description": getattr(step, "description", "")
            })

    _generate_single_process_flow(
        interface=interface,
        output_file=output_file,
        steps=all_steps,
        first_page=True,
        last_page=True
    )