def analyze_adapters(interface):

    # print("\n========== Adapter Analyzer ==========\n")

    PURPOSES = {

        "ExternalCall": (
            "Request Reply",
            "Invokes an external service",
            "Receiver"
        ),

        "Mapping": (
            "Message Mapping",
            "Transforms message payload",
            "Internal"
        ),

        "Script": (
            "Groovy Script",
            "Executes custom Groovy logic",
            "Internal"
        ),

        "Enricher": (
            "Content Modifier",
            "Creates or modifies headers, properties or body",
            "Internal"
        ),

        "Splitter": (
            "General Splitter",
            "Splits one message into multiple messages",
            "Internal"
        ),

        "SequentialMulticast": (
            "Sequential Multicast",
            "Routes the message through multiple branches sequentially",
            "Internal"
        ),

        "JsonToXmlConverter": (
            "JSON to XML Converter",
            "Converts JSON payload into XML",
            "Internal"
        ),

        "XmlToJsonConverter": (
            "XML to JSON Converter",
            "Converts XML payload into JSON",
            "Internal"
        ),

        "Decoder": (
            "Base64 Decoder",
            "Decodes Base64 encoded content",
            "Internal"
        )

    }

    for component in interface.components:

        activity = component.properties.get("activityType", "")

        if activity in PURPOSES:

            component.analysis["component_type"] = PURPOSES[activity][0]

            component.analysis["purpose"] = PURPOSES[activity][1]

            component.analysis["direction"] = PURPOSES[activity][2]

    # print("Component analysis completed.\n")

    for component in interface.components:

        if component.analysis:

            print(component.name)

            for key, value in component.analysis.items():

                print(f"   {key} = {value}")

            print()