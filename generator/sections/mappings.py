def add_mappings(document, interface):

    document.add_heading(
        "Message Mappings",
        level=1
    )

    mappings = interface.resources.get(
        "mapping",
        []
    )

    if not mappings:

        document.add_paragraph(
            "No message mappings are used in this integration flow."
        )

        return

    table = document.add_table(
        rows=1,
        cols=4
    )

    table.style = "Table Grid"

    header = table.rows[0].cells

    header[0].text = "No."

    header[1].text = "Mapping Name"

    header[2].text = "File"

    header[3].text = "Purpose"

    for index, mapping in enumerate(mappings, start=1):

        row = table.add_row().cells

        row[0].text = str(index)

        row[1].text = mapping.get(
            "name",
            "Unknown"
        )

        row[2].text = mapping.get(
            "path",
            mapping.get(
                "name",
                "-"
            )
        )

        row[3].text = (
            "Message transformation between source and target formats"
        )