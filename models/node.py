from dataclasses import dataclass, field


@dataclass
class Node:

    id: str = ""

    name: str = ""

    type: str = ""

    process: str = ""

    properties: dict = field(default_factory=dict)

    inputs: list = field(default_factory=list)

    outputs: list = field(default_factory=list)

    resources: list = field(default_factory=list)

    description: str = ""