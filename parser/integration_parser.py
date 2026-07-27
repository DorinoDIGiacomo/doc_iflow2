from collections import defaultdict


def parse_integration(root, interface):

    print("\n========== Integration Parser ==========\n")

    values = defaultdict(set)

    # ---------------------------------------------------------
    # Read all SAP properties from the iFlow
    # ---------------------------------------------------------

    for prop in root.xpath('//*[local-name()="property"]'):

        key = prop.xpath('./*[local-name()="key"]/text()')
        value = prop.xpath('./*[local-name()="value"]/text()')

        if not key or not value:
            continue

        key = key[0].strip()
        value = value[0].strip()

        if value:
            values[key].add(value)

    # ---------------------------------------------------------
    # Sender Adapter Detection
    # ---------------------------------------------------------

    transport_protocols = set()

    transport_protocols.update(values["TransportProtocol"])
    transport_protocols.update(values["transportProtocol"])

    for protocol in transport_protocols:

        protocol_upper = protocol.upper()

        if "SFTP" in protocol_upper:

            interface.sender_adapters.append("SFTP")
            interface.sender_systems.append("SFTP Server")

        elif "FTP" in protocol_upper:

            interface.sender_adapters.append("FTP")
            interface.sender_systems.append("FTP Server")

        elif "FILE" in protocol_upper:

            interface.sender_adapters.append("File")
            interface.sender_systems.append("File System")

        elif "MAIL" in protocol_upper:

            interface.sender_adapters.append("Mail")
            interface.sender_systems.append("Mail Server")

        elif "JMS" in protocol_upper:

            interface.sender_adapters.append("JMS")
            interface.sender_systems.append("JMS Queue")

        elif "SOAP" in protocol_upper:

            interface.sender_adapters.append("SOAP")
            interface.sender_systems.append("SOAP Service")

        elif "ODATA" in protocol_upper:

            interface.sender_adapters.append("OData")
            interface.sender_systems.append("SAP S/4HANA")

        elif "IDOC" in protocol_upper:

            interface.sender_adapters.append("IDoc")
            interface.sender_systems.append("SAP ECC")

    # ---------------------------------------------------------
    # Receiver Detection
    # ---------------------------------------------------------

    if values["httpAddressWithoutQuery"] or values["address"]:

        interface.receiver_adapters.append("HTTP")
        interface.receiver_systems.append("SAP S/4HANA")

    if values["processDirectAddress"]:

        interface.receiver_adapters.append("ProcessDirect")
        interface.receiver_systems.append("SAP Integration Suite")

    # ---------------------------------------------------------
    # Protocols
    # ---------------------------------------------------------

    for protocol in transport_protocols:
        interface.protocols.append(protocol)

    if values["httpAddressWithoutQuery"]:
        interface.protocols.append("HTTP")

    if values["address"]:
        interface.protocols.append("HTTP")

    # ---------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------

    for auth in values["authentication"]:
        interface.authentication.append(auth)

    for auth in values["authenticationMethod"]:
        interface.authentication.append(auth)

    # ---------------------------------------------------------
    # Endpoints
    # ---------------------------------------------------------

    for endpoint in values["host"]:
        interface.endpoints.append(endpoint)

    for endpoint in values["address"]:
        interface.endpoints.append(endpoint)

    for endpoint in values["httpAddressWithoutQuery"]:
        interface.endpoints.append(endpoint)

    for endpoint in values["processDirectAddress"]:
        interface.endpoints.append(endpoint)

    # ---------------------------------------------------------
    # Message Format Detection
    # ---------------------------------------------------------

    if interface.resources.get("xsd"):
        interface.message_formats.append("XML")

    if interface.resources.get("edmx"):
        interface.message_formats.append("OData")

    if interface.resources.get("mapping"):
        interface.message_formats.append("Mapped Payload")

    # ---------------------------------------------------------
    # Remove Duplicates
    # ---------------------------------------------------------

    interface.sender_adapters = sorted(set(interface.sender_adapters))
    interface.receiver_adapters = sorted(set(interface.receiver_adapters))

    interface.sender_systems = sorted(set(interface.sender_systems))
    interface.receiver_systems = sorted(set(interface.receiver_systems))

    interface.protocols = sorted(set(interface.protocols))
    interface.authentication = sorted(set(interface.authentication))
    interface.endpoints = sorted(set(interface.endpoints))
    interface.message_formats = sorted(set(interface.message_formats))

    # ---------------------------------------------------------
    # Display Summary
    # ---------------------------------------------------------

    print("Sender Adapters")
    print(interface.sender_adapters)

    print()

    print("Receiver Adapters")
    print(interface.receiver_adapters)

    print()

    print("Sender Systems")
    print(interface.sender_systems)

    print()

    print("Receiver Systems")
    print(interface.receiver_systems)

    print()

    print("Protocols")
    print(interface.protocols)

    print()

    print("Authentication")
    print(interface.authentication)

    print()

    print("Message Formats")
    print(interface.message_formats)

    print()

    print("Endpoints")

    for endpoint in interface.endpoints:
        print(endpoint)