def analyze_connections(interface):

    # print("\n========== Flow Analyzer ==========\n")

    # Reset
    for component in interface.components:

        component.analysis["incoming"] = []
        component.analysis["outgoing"] = []

    lookup = {
        component.id: component
        for component in interface.components
    }

    for connection in interface.connections:

        if connection.source in lookup:

            lookup[connection.source].analysis["outgoing"].append(
                lookup.get(connection.target).name
                if connection.target in lookup else connection.target
            )

        if connection.target in lookup:

            lookup[connection.target].analysis["incoming"].append(
                lookup.get(connection.source).name
                if connection.source in lookup else connection.source
            )

    # print("Connection analysis completed.")