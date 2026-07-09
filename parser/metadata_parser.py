BPMN = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"
}


def parse_metadata(root, interface):

    print("\n========== Metadata Parser ==========\n")

    # --------------------------------------------------
    # Interface Name
    # --------------------------------------------------

    # Keep the interface name already assigned
    # (for example, from the ZIP filename in main.py)

    if not interface.name:

        metadata_name = root.get("name")

        if metadata_name and metadata_name.strip():

            interface.name = metadata_name.strip()

    if not interface.name:

        process = root.find(
            ".//bpmn:process",
            namespaces=BPMN
        )

        if process is not None:

            process_name = process.get("name")

            if (
                process_name
                and process_name.strip()
                and process_name.lower() not in [
                    "integration process",
                    "process",
                    "main process"
                ]
            ):

                interface.name = process_name.strip()

    if not interface.name:

        interface.name = "Unknown Interface"

    # --------------------------------------------------
    # Version
    # --------------------------------------------------

    interface.version = root.get(
        "version",
        "1.0"
    )

    # --------------------------------------------------
    # Description
    # --------------------------------------------------

    documentation = root.find(
        ".//bpmn:documentation",
        namespaces=BPMN
    )

    if (
        documentation is not None
        and documentation.text
    ):

        interface.description = documentation.text.strip()

    else:

        interface.description = ""

    print(f"Name        : {interface.name}")
    print(f"Version     : {interface.version}")
    print(f"Description : {interface.description}")