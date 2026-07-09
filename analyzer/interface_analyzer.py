def analyze_interface(interface):

    # print("\n========== Interface Analyzer ==========\n")

    analysis = {}

    # ---------------------------------
    # Counts
    # ---------------------------------

    analysis["component_count"] = len(interface.components)

    analysis["connection_count"] = len(interface.connections)

    analysis["groovy_count"] = len(interface.resources["groovy"])

    analysis["mapping_count"] = len(interface.resources["mapping"])

    analysis["xsd_count"] = len(interface.resources["xsd"])

    analysis["wsdl_count"] = len(interface.resources["wsdl"])

    analysis["edmx_count"] = len(interface.resources["edmx"])

    # ---------------------------------
    # Complexity
    # ---------------------------------

    component_count = analysis["component_count"]

    if component_count < 15:

        analysis["complexity"] = "Low"

    elif component_count <= 30:

        analysis["complexity"] = "Medium"

    else:

        analysis["complexity"] = "High"

    # ---------------------------------
    # Feature Detection
    # ---------------------------------

    analysis["contains_groovy"] = analysis["groovy_count"] > 0

    analysis["contains_mapping"] = analysis["mapping_count"] > 0

    analysis["contains_exception_subprocess"] = False

    analysis["contains_splitter"] = False

    analysis["contains_multicast"] = False

    # ---------------------------------
    # Scan Components
    # ---------------------------------

    for component in interface.components:

        category = component.category.lower()

        if "exception" in category:

            analysis["contains_exception_subprocess"] = True

        if "splitter" in category:

            analysis["contains_splitter"] = True

        if "multicast" in category:

            analysis["contains_multicast"] = True
    
    # ---------------------------------
    # Business Summary
    # ---------------------------------

    source_adapter = "Unknown"
    target_adapter = "Unknown"

    for component in interface.components:

        category = component.category.lower()

        if category == "start event":
            source_adapter = "Start Event"

        elif "request reply" in category:
            target_adapter = "External System"

    analysis["source_system"] = source_adapter

    analysis["target_system"] = target_adapter

    analysis["integration_pattern"] = (
        "Synchronous"
        if target_adapter != "Unknown"
        else "Unknown"
    )

    analysis["primary_flow"] = []

    for component in interface.components:

        if component.category in [
            "Content Modifier",
            "Groovy Script",
            "Message Mapping",
            "Request Reply",
            "General Splitter",
            "Iterating Splitter",
            "Router",
            "End Event"
        ]:

            analysis["primary_flow"].append(
                component.category
            )

    # ---------------------------------
    # Store
    # ---------------------------------

    interface.analysis = analysis

    # ---------------------------------
    # Display
    # ---------------------------------

    for key, value in analysis.items():

        print(f"{key:35} : {value}")