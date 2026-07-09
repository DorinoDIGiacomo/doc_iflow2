from models.document_model import DocumentModel


class DocumentBuilder:

    @staticmethod
    def build(interface):

        document = DocumentModel()

        # =====================================
        # Basic Information
        # =====================================

        document.interface_name = interface.name

        document.interface_type = getattr(
            interface,
            "type",
            "SAP CPI Integration"
        )

        # =====================================
        # Components
        # =====================================

        document.components = getattr(
            interface,
            "components",
            []
        )

        # =====================================
        # Properties
        # =====================================

        document.properties = getattr(
            interface,
            "properties",
            {}
        )

        # =====================================
        # Metadata
        # =====================================

        document.metadata = {

            "component_count": len(
                document.components
            ),

            "property_count": len(
                document.properties
            )
        }
            # =====================================
        # Diagram Data
        # =====================================

        phases = []

        previous = None

        for component in document.components:

            name = component.component_type

            # ---------- Business Mapping ----------

            if "Content Modifier" in name:
                phase = "Prepare Message"

            elif "Groovy" in name:
                phase = "Business Logic"

            elif "Mapping" in name:
                phase = "Transform Business Data"

            elif "Router" in name:
                phase = "Route Message"

            elif "Splitter" in name:
                phase = "Split Processing"

            elif "Gather" in name:
                phase = "Merge Results"

            elif "Request Reply" in name:
                phase = "Invoke Target System"

            elif "End Event" in name:
                phase = "Process Complete"

            elif "Start Event" in name:
                phase = "Receive Request"

            else:
                continue

            # Remove duplicate consecutive phases

            if phase == previous:
                continue

            previous = phase

            phases.append(
                {
                    "title": phase,
                    "category": "Process"
                }
            )

        document.diagram_data = {

            "phases": phases

        }

        return document