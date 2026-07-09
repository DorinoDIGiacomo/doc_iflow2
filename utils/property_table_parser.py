from lxml import etree


def parse_property_table(xml_string):
    """
    Parses CPI propertyTable/headerTable XML into a list of dictionaries.
    """

    if not xml_string:
        return None

    if "<row>" not in xml_string:
        return None

    try:

        root = etree.fromstring(
            f"<root>{xml_string}</root>"
        )

        rows = []

        for row in root.findall("row"):

            data = {}

            for cell in row.findall("cell"):

                key = cell.get("id", "Value")

                value = (cell.text or "").strip()

                data[key] = value

            rows.append(data)

        return rows

    except Exception:

        return None