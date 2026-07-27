from dataclasses import dataclass, field


@dataclass
class Interface:

    # ==========================================================
    # Basic Information
    # ==========================================================
    name: str = ""
    version: str = ""
    description: str = ""

    # Package / Artifact Information
    package_name: str = ""
    package_id: str = ""
    artifact_id: str = ""
    namespace: str = ""

    # Runtime Information
    runtime: str = "SAP Integration Suite"

    # ==========================================================
    # Original iFlow XML
    # ==========================================================
    iflow_xml: str = ""

    # ==========================================================
    # Parsed Components
    # ==========================================================
    components: list = field(default_factory=list)

    # ==========================================================
    # Process Flow
    # ==========================================================
    connections: list = field(default_factory=list)

    # ==========================================================
    # Adapter Information
    # ==========================================================
    sender_adapters: list = field(default_factory=list)
    receiver_adapters: list = field(default_factory=list)

    # ==========================================================
    # External Systems
    # ==========================================================
    sender_systems: list = field(default_factory=list)
    receiver_systems: list = field(default_factory=list)
    external_systems: list = field(default_factory=list)

    # ==========================================================
    # Connectivity Information
    # ==========================================================
    protocols: list = field(default_factory=list)
    authentication: list = field(default_factory=list)
    endpoints: list = field(default_factory=list)

    # ==========================================================
    # Message Information
    # ==========================================================
    message_formats: list = field(default_factory=list)

    # ==========================================================
    # ZIP Resources
    # ==========================================================
    resources: dict = field(default_factory=lambda: {
        "groovy": [],
        "mapping": [],
        "xsd": [],
        "wsdl": [],
        "edmx": [],
        "properties": [],
        "other": []
    })

    # ==========================================================
    # Resource Summary
    # (Automatically populated by metadata parser)
    # ==========================================================
    groovy_scripts: list = field(default_factory=list)
    mappings: list = field(default_factory=list)
    xsd_files: list = field(default_factory=list)
    wsdl_files: list = field(default_factory=list)
    edmx_files: list = field(default_factory=list)

    # ==========================================================
    # Statistics
    # ==========================================================
    component_count: int = 0
    adapter_count: int = 0

    statistics: dict = field(default_factory=dict)

    # ==========================================================
    # Technical Metadata
    # ==========================================================
    metadata: dict = field(default_factory=dict)

    # ==========================================================
    # Component Analysis
    # ==========================================================
    analysis: dict = field(default_factory=dict)

    # ==========================================================
    # Future Extensions
    # ==========================================================
    adapter_summary: dict = field(default_factory=dict)