from models.connection import Connection

BPMN = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"
}


def parse_flows(root, interface):

    print("\n========== Flow Parser ==========\n")

    for process in root.xpath("//bpmn:process", namespaces=BPMN):

        for flow in process.xpath("./bpmn:sequenceFlow", namespaces=BPMN):

            connection = Connection()

            connection.id = flow.get("id", "")

            connection.source = flow.get("sourceRef", "")

            connection.target = flow.get("targetRef", "")

            connection.name = flow.get("name", "")

            interface.connections.append(connection)

    print(f"Connections Parsed : {len(interface.connections)}")