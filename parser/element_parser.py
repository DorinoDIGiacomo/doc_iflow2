from models.component import Component


def classify_component(name: str, bpmn_type: str) -> str:

    name = name or ""

    if "Groovy" in name:
        return "Groovy Script"

    elif "Message Mapping" in name:
        return "Message Mapping"

    elif "Content Modifier" in name or name.startswith("CM_"):
        return "Content Modifier"

    elif "General Splitter" in name:
        return "General Splitter"

    elif "Iterating Splitter" in name:
        return "Iterating Splitter"

    elif "JSON to XML" in name:
        return "JSON to XML Converter"

    elif "XML to JSON" in name:
        return "XML to JSON Converter"

    elif "Base64" in name:
        return "Base64 Decoder"

    elif "Request Reply" in name:
        return "Request Reply"

    elif "Sequential Multicast" in name:
        return "Sequential Multicast"

    elif "Parallel Multicast" in name:
        return "Parallel Multicast"

    elif "Exception" in name:
        return "Exception Subprocess"

    elif bpmn_type == "startEvent":
        return "Start Event"

    elif bpmn_type == "endEvent":
        return "End Event"

    else:
        return bpmn_type


def parse_element(element, process_id):

    component = Component()

    component.id = element.get("id", "")
    component.name = element.get("name", "")
    component.process = process_id

    component.bpmn_type = element.tag.split("}")[-1]

    component.category = classify_component(
        component.name,
        component.bpmn_type
    )

    return component