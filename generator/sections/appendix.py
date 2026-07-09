from datetime import datetime


def add_appendix(document, interface):

    document.add_heading(
        "Appendix",
        level=1
    )

    document.add_heading(
        "A.1 Document Generation Information",
        level=2
    )

    table = document.add_table(
        rows=6,
        cols=2
    )

    table.style = "Table Grid"

    table.cell(0, 0).text = "Generator"
    table.cell(0, 1).text = "AI SAP CPI Solution Design Generator"

    table.cell(1, 0).text = "Generation Date"
    table.cell(1, 1).text = datetime.now().strftime("%d-%m-%Y %H:%M")

    table.cell(2, 0).text = "Interface"
    table.cell(2, 1).text = interface.name

    table.cell(3, 0).text = "Version"
    table.cell(3, 1).text = interface.version or "1.0"

    table.cell(4, 0).text = "Total Components"
    table.cell(4, 1).text = str(len(interface.components))

    table.cell(5, 0).text = "Total Connections"
    table.cell(5, 1).text = str(len(interface.connections))

    document.add_paragraph()

    # =====================================================
    # Resource Summary
    # =====================================================

    document.add_heading(
        "A.2 Resource Summary",
        level=2
    )

    resource_table = document.add_table(
        rows=1,
        cols=2
    )

    resource_table.style = "Table Grid"

    header = resource_table.rows[0].cells

    header[0].text = "Resource Type"
    header[1].text = "Count"

    resource_summary = [

        ("Groovy Scripts", len(interface.resources.get("groovy", []))),
        ("Message Mappings", len(interface.resources.get("mapping", []))),
        ("XSD Files", len(interface.resources.get("xsd", []))),
        ("WSDL Files", len(interface.resources.get("wsdl", []))),
        ("EDMX Files", len(interface.resources.get("edmx", []))),
        ("Properties Files", len(interface.resources.get("properties", []))),
        ("Other Files", len(interface.resources.get("other", [])))

    ]

    for name, count in resource_summary:

        row = resource_table.add_row().cells

        row[0].text = name

        row[1].text = str(count)

    document.add_paragraph()

    # =====================================================
    # Disclaimer
    # =====================================================

    document.add_heading(
        "A.3 Disclaimer",
        level=2
    )

    document.add_paragraph(

        "This Solution Design Document has been generated from the "
        "SAP Integration Suite (SAP CPI) integration artifacts and "
        "their associated metadata. The document is intended to "
        "provide a structured technical overview of the interface. "
        "Any business-specific information should be reviewed and "
        "validated before being used for implementation or production "
        "documentation."

    )