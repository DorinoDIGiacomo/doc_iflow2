import json
import os


def build_json(interface):

    data = {

        "interface": {
            "name": interface.name,
            "version": interface.version,
            "description": interface.description
        },

        "components": [],

        "connections": [],

        "resources": interface.resources
    }

    # Components
    for component in interface.components:

        data["components"].append({

            "id": component.id,
            "name": component.name,
            "category": component.category,
            "bpmn_type": component.bpmn_type,
            "process": component.process,
            "properties": component.properties

        })

    # Connections
    for connection in interface.connections:

        data["connections"].append({

            "id": connection.id,
            "source": connection.source,
            "target": connection.target,
            "name": connection.name

        })

    # Create output folder

    os.makedirs("output", exist_ok=True)

    output_file = "output/interface.json"

    with open(output_file, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=4)

    print(f"\nJSON written to : {output_file}")

    return data