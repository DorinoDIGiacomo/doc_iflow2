from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class DocumentModel:

    # ==========================
    # Basic Information
    # ==========================

    interface_name: str = ""

    interface_type: str = ""

    source_system: str = ""

    target_system: str = ""

    communication_type: str = ""

    # ==========================
    # Parser Information
    # ==========================

    components: List[Any] = field(default_factory=list)

    adapters: List[str] = field(default_factory=list)

    properties: Dict = field(default_factory=dict)

    # ==========================
    # AI Generated Sections
    # ==========================

    ai_sections: Dict = field(default_factory=dict)

    # ==========================
    # Diagram
    # ==========================

    diagram_data: Dict = field(default_factory=dict)

    diagram_image: str = ""

    # ==========================
    # Metadata
    # ==========================

    metadata: Dict = field(default_factory=dict)