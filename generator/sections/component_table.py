def add_component_table(document, interface):

    document.add_heading(
        "Component Overview",
        level=1
    )

    table = document.add_table(
        rows=1,
        cols=6
    )

    table.style = "Table Grid"

    header = table.rows[0].cells

    header[0].text = "No."

    header[1].text = "Component"

    header[2].text = "Category"

    header[3].text = "Direction"

    header[4].text = "Process"

    header[5].text = "Purpose"

    for index, component in enumerate(interface.components, start=1):

        analysis = component.analysis or {}

        row = table.add_row().cells

        row[0].text = str(index)

        row[1].text = component.name

        row[2].text = component.category

        row[3].text = analysis.get(
            "direction",
            "-"
        )

        row[4].text = component.process

        row[5].text = analysis.get(
            "purpose",
            "-"
        )