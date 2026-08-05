import re


def build_interface_knowledge(interface):
    """
    Builds a normalized business knowledge model from the parsed interface.
    This model is later supplied to the AI prompt so that the LLM reasons
    from business facts instead of raw parser metadata.
    """

    knowledge = {
        "business_object": detect_business_object(interface.name),
        "integration_pattern": detect_integration_pattern(interface),
        "communication_type": detect_communication_type(interface),
        "sender": sorted(interface.sender_systems),
        "receiver": sorted(interface.receiver_systems),
        "protocols": sorted(interface.protocols),
        "message_formats": sorted(interface.message_formats),
        "transformations": detect_transformations(interface),
        "routing": has_component(interface, "router"),
        "split_processing": has_component(interface, "splitter"),
        "multicast": has_component(interface, "multicast"),
        "aggregation": has_component(interface, "gather"),
        "request_reply": has_component(interface, "request reply"),
        "exception_handling": has_component(interface, "exception"),
        "groovy_used": len(interface.resources.get("groovy", [])) > 0,
        "message_mapping_used": len(interface.resources.get("mapping", [])) > 0,
        "xsd_used": len(interface.resources.get("xsd", [])) > 0,
        "wsdl_used": len(interface.resources.get("wsdl", [])) > 0
    }

    return knowledge


# ==========================================================
# Helper Functions
# ==========================================================

def has_component(interface, keyword):
    keyword = keyword.lower()

    return any(
        keyword in component.category.lower()
        for component in interface.components
    )


def detect_communication_type(interface):

    if has_component(interface, "request reply"):
        return "Synchronous"

    return "Asynchronous"


def detect_integration_pattern(interface):

    sender = " ".join(interface.sender_adapters).lower()
    receiver = " ".join(interface.receiver_adapters).lower()

    if "sftp" in sender and "odata" in receiver:
        return "File to OData"

    if "sftp" in sender and "http" in receiver:
        return "File to HTTP"

    if "http" in sender and "odata" in receiver:
        return "API to OData"

    if "http" in sender and "http" in receiver:
        return "API to API"

    return "Point-to-Point Integration"


def detect_transformations(interface):

    transformations = []

    if interface.resources.get("mapping"):
        transformations.append("Message Mapping")

    if has_component(interface, "converter"):
        transformations.append("Payload Conversion")

    if interface.resources.get("groovy"):
        transformations.append("Custom Groovy Processing")

    return transformations


def detect_business_object(interface_name):

    name = interface_name.lower()

    patterns = {
        "Sales Order": [
            "sales order",
            "salesorder"
        ],
        "Debit Memo": [
            "debit memo",
            "debitmemo"
        ],
        "Invoice": [
            "invoice",
            "billing"
        ],
        "Business Partner": [
            "business partner",
            "bp"
        ],
        "Material": [
            "material"
        ],
        "Purchase Order": [
            "purchase order",
            "po"
        ],
        "Delivery": [
            "delivery"
        ]
    }

    for business_object, keywords in patterns.items():

        for keyword in keywords:

            if keyword in name:
                return business_object

    return "Business Document"