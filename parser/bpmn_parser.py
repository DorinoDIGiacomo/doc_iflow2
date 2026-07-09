from parser.element_parser import parse_element

BPMN = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"
}

SKIP_TAGS = {
    "sequenceFlow",
    "extensionElements",
    "documentation"
}


def parse_bpmn(root, interface):

    print("\n========== BPMN Parser ==========\n")

    interface.components.clear()

    for process in root.xpath("//bpmn:process", namespaces=BPMN):

        process_id = process.get("id")
        process_name = process.get("name", "Unnamed")

        print(f"Process : {process_name}")

        for element in process:

            tag = element.tag.split("}")[-1]

            if tag in SKIP_TAGS:
                continue

            component = parse_element(
                element,
                process_id
            )

            interface.components.append(component)

    print("\n========== Components ==========\n")

    for component in interface.components:

        print(
            f"{component.category:30} {component.name}"
        )