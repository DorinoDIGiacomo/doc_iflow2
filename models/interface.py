from dataclasses import dataclass, field


@dataclass
class Interface:

    # -------------------------------
    # Basic Information
    # -------------------------------
    name: str = ""
    version: str = ""
    description: str = ""

    # -------------------------------
    # Original iFlow XML
    # -------------------------------
    iflow_xml: str = ""

    # -------------------------------
    # Parsed Components
    # -------------------------------
    components: list = field(default_factory=list)

    # -------------------------------
    # Process Flow
    # -------------------------------
    connections: list = field(default_factory=list)

    # -------------------------------
    # ZIP Resources
    # -------------------------------
    resources: dict = field(default_factory=lambda: {
        "groovy": [],
        "mapping": [],
        "xsd": [],
        "wsdl": [],
        "edmx": [],
        "properties": [],
        "other": []
    })

    # -------------------------------
    # Additional Information
    # -------------------------------
    statistics: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    # -------------------------------
    # Analysis Results
    # -------------------------------
    analysis: dict = field(default_factory=dict)
    