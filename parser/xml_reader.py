from lxml import etree


def parse_iflow(interface):

    root = etree.fromstring(interface.iflow_xml.encode("utf-8"))

    print("\n========== Root Information ==========\n")

    print("Root Tag:", root.tag)

    print("\nRoot Attributes:")

    for key, value in root.attrib.items():
        print(f"{key} = {value}")

    print("\n========== Root Children ==========\n")

    for child in root:

        tag = child.tag.split("}")[-1]

        print(f"\n{tag}")

        if child.attrib:
            for k, v in child.attrib.items():
                print(f"   {k} = {v}")

    return root