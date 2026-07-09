from lxml import etree

BPMN = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"
}


def parse_properties(root, interface):

    print("\n========== Property Parser ==========\n")

    # Fast lookup by component ID
    component_lookup = {
        component.id: component
        for component in interface.components
    }

    property_count = 0

    for process in root.xpath("//bpmn:process", namespaces=BPMN):

        for element in process:

            component_id = element.get("id")

            if component_id not in component_lookup:
                continue

            component = component_lookup[component_id]

            extension = element.find(
                "{http://www.omg.org/spec/BPMN/20100524/MODEL}extensionElements"
            )

            if extension is None:
                continue

            for prop in extension:

                key = None
                value = None

                for child in prop:

                    tag = child.tag.split("}")[-1].lower()

                    text = (child.text or "").strip()

                    if tag == "key":
                        key = text

                    elif tag == "value":
                        value = text

                if key:

                    component.properties[key] = value

                    property_count += 1

    print(f"Properties Parsed : {property_count}")

    print(f"Properties Parsed : {property_count}")

    print("\n========== Component Properties ==========\n")

    for component in interface.components:

        if component.properties:

            print(component.name)

            for key, value in component.properties.items():

                print(f"   {key} = {value}")

            print()