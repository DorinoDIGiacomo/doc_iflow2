def add_groovy(document, interface):

    document.add_heading(
        "Groovy Scripts",
        level=1
    )

    groovy_scripts = interface.resources.get(
        "groovy",
        []
    )

    if not groovy_scripts:

        document.add_paragraph(
            "No Groovy scripts are used in this integration flow."
        )

        return

    table = document.add_table(
        rows=1,
        cols=4
    )

    table.style = "Table Grid"

    header = table.rows[0].cells

    header[0].text = "No."

    header[1].text = "Script Name"

    header[2].text = "File"

    header[3].text = "Purpose"

    for index, script in enumerate(groovy_scripts, start=1):

        row = table.add_row().cells

        row[0].text = str(index)

        row[1].text = script.get(
            "name",
            "Unknown"
        )

        row[2].text = script.get(
            "path",
            script.get(
                "name",
                "-"
            )
        )

        row[3].text = (
            "Custom transformation / validation logic"
        )