def add_resources(document, interface):

    document.add_heading(
        "Resources",
        level=1
    )

    resources = [

        ("Groovy Scripts", len(interface.resources["groovy"])),

        ("Mappings", len(interface.resources["mapping"])),

        ("XSD Files", len(interface.resources["xsd"])),

        ("WSDL Files", len(interface.resources["wsdl"])),

        ("EDMX Files", len(interface.resources["edmx"])),

        ("Properties", len(interface.resources["properties"]))
    ]

    table = document.add_table(
        rows=1,
        cols=2
    )

    table.style = "Table Grid"

    hdr = table.rows[0].cells

    hdr[0].text = "Resource"

    hdr[1].text = "Count"

    for name, count in resources:

        row = table.add_row().cells

        row[0].text = name

        row[1].text = str(count)

    for category in [
        "groovy",
        "mapping",
        "xsd",
        "wsdl",
        "edmx"
    ]:

        document.add_heading(category.upper(), level=2)

        resources = interface.resources.get(category, [])

        if not resources:

            document.add_paragraph("None")

            continue

    for resource in resources:

        document.add_paragraph(
            resource["name"],
            style="List Bullet"
        )