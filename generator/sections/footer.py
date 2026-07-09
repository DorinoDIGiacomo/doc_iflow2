from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def add_footer(document):

    section = document.sections[0]

    # Keep a separate footer for the cover page
    section.different_first_page_header_footer = True

    footer = section.footer

    paragraph = footer.paragraphs[0]

    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)

    run = paragraph.add_run("Page-")

    run.font.name = "Calibri"
    run.font.size = Pt(10)

    # Dynamic page number
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")

    r = OxmlElement("w:r")
    fld.append(r)

    paragraph._p.append(fld)