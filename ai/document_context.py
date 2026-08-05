import json
from analyzer.interface_knowledge_builder import build_interface_knowledge

def build_document_context(interface):

    components = []

    adapters = set()

    mappings = []

    groovy_scripts = []

    converters = []

    request_reply = 0
    splitters = 0
    multicast = 0

    routers = 0
    content_modifiers = 0

    exception_subprocess = False

    start_events = 0
    end_events = 0

    sender_systems = set()
    receiver_systems = set()

    # =====================================================
    # Component Analysis
    # =====================================================

    for component in interface.components:

        analysis = component.analysis or {}

        direction = analysis.get("direction", "")

        purpose = analysis.get("purpose", "")

        incoming = analysis.get("incoming", [])

        outgoing = analysis.get("outgoing", [])

        component_info = {

            "name": component.name,

            "type": component.category,

            "process": component.process,

            "purpose": purpose,

            "direction": direction,

            "incoming": incoming,

            "outgoing": outgoing,

            "properties": component.properties

        }

        components.append(component_info)

        category = component.category.lower()

        # =================================================
        # Statistics
        # =================================================

        if "request reply" in category:
            request_reply += 1

        elif "splitter" in category:
            splitters += 1

        elif "multicast" in category:
            multicast += 1

        elif "router" in category:
            routers += 1

        elif "content modifier" in category:
            content_modifiers += 1

        elif "groovy" in category:
            groovy_scripts.append(component.name)

        elif "mapping" in category:
            mappings.append(component.name)

        elif "converter" in category:
            converters.append(component.name)

        if "exception" in category:
            exception_subprocess = True

        if "start event" in category:
            start_events += 1

        if "end event" in category:
            end_events += 1

        if direction:
            adapters.add(direction)

        # =================================================
        # Try to infer systems
        # =================================================

        if "sender" in direction.lower():

            sender_systems.add(component.name)

        if "receiver" in direction.lower():

            receiver_systems.add(component.name)

    # =====================================================
    # Integration Pattern
    # =====================================================

    if request_reply > 0:

        integration_pattern = "Synchronous"

    else:

        integration_pattern = "Asynchronous"

    # =====================================================
    # Build Knowledge Model
    # =====================================================

    knowledge = build_interface_knowledge(interface)

    # =====================================================
    # Context
    # =====================================================
    
    context = {

        "document": {

        "title": interface.name,

        "document_type": "SAP Integration Suite Solution Design Document",

        "version": interface.version

        },
        
        "knowledge": knowledge,

        "interface": {

            "name": interface.name,

            "version": interface.version,

            "description": interface.description,

            "runtime": interface.runtime,

            "package_name": interface.package_name,

            "package_id": interface.package_id,

            "artifact_id": interface.artifact_id,

            "namespace": interface.namespace

        },

        "integration": {

            "pattern": integration_pattern,

            "sender_systems": interface.sender_systems,

            "receiver_systems": interface.receiver_systems,

            "external_systems": interface.external_systems,

            "sender_adapters": interface.sender_adapters,

            "receiver_adapters": interface.receiver_adapters,

            "protocols": interface.protocols,

            "authentication": interface.authentication,

            "message_formats": interface.message_formats,

            "endpoints": interface.endpoints

        },

        "statistics": {

            "component_count": len(interface.components),

            "connection_count": len(interface.connections),

            "mapping_count": len(interface.resources["mapping"]),

            "groovy_count": len(interface.resources["groovy"]),

            "xsd_count": len(interface.resources["xsd"]),

            "wsdl_count": len(interface.resources["wsdl"]),

            "edmx_count": len(interface.resources["edmx"])

        },

        "architecture": {

            "request_reply_steps": request_reply,

            "splitters": splitters,

            "multicast": multicast,

            "routers": routers,

            "content_modifiers": content_modifiers,

            "exception_subprocess": exception_subprocess,

            "start_events": start_events,

            "end_events": end_events
        
        },
            
        "integration_summary": {

            "total_components": len(interface.components),

            "total_connections": len(interface.connections),

            "total_sender_systems": len(interface.sender_systems),

            "total_receiver_systems": len(interface.receiver_systems),

            "total_sender_adapters": len(interface.sender_adapters),

            "total_receiver_adapters": len(interface.receiver_adapters),

            "total_protocols": len(interface.protocols),

            "total_message_formats": len(interface.message_formats)

        },

        "resources": interface.resources,

        "mappings": mappings,

        "groovy_scripts": groovy_scripts,

        "converters": converters,

        "adapter_directions": sorted(list(adapters)),

        "components": components,

        "connections": [

            {

                "source": connection.source,

                "target": connection.target

            }

            for connection in interface.connections

        ]

    }

    return context


def context_to_json(interface):

    return json.dumps(

        build_document_context(interface),

        indent=4,

        ensure_ascii=False

    )