from dataclasses import dataclass, field


@dataclass
class Component:

    # -------------------------------
    # Basic Information
    # -------------------------------
    id: str = ""

    name: str = ""

    bpmn_type: str = ""

    category: str = ""

    process: str = ""

    # -------------------------------
    # Raw Properties (Parsed from XML)
    # -------------------------------
    properties: dict = field(default_factory=dict)

    # -------------------------------
    # Analysis Results
    # -------------------------------
    analysis: dict = field(default_factory=dict)