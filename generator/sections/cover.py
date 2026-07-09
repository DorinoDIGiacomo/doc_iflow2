from datetime import datetime
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt

def add_cover(document, interface):

    # =====================================================
    # Main Title
    # =====================================================

    title = document.add_heading(level=0)

    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    run = title.add_run(
        "SAP Integration Suite\n"
        "Interface Design Document"
    )

    run.bold = True
    run.font.size = Pt(26)
    run.font.name = "Times New Roman"

    document.add_paragraph()

    # =====================================================
    # Information Table
    # =====================================================

    table = document.add_table(rows=3, cols=2)

    table.style = "Table Grid"

    table.cell(0, 0).text = "Interface Name"
    table.cell(0, 1).text = interface.name

    table.cell(1, 0).text = "Generated On"
    table.cell(1, 1).text = datetime.now().strftime("%d-%m-%Y")

    table.cell(2, 0).text = "Platform"
    table.cell(2, 1).text = "SAP Integration Suite (Cloud Integration)"

    document.add_paragraph()

    # =====================================================
    # Footer Text
    # =====================================================

    footer = document.add_paragraph()

    footer.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    footer.add_run(
        "This document provides the solution design for the "
        f"'{interface.name}' interface. "
        "It has been automatically generated using the SAP CPI "
        "integration artifacts and AI-assisted documentation. "
        "It serves as a technical reference for understanding "
        "the interface design and implementation."

    ).italic = True

    document.add_page_break()