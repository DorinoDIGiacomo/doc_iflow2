from dataclasses import dataclass


@dataclass
class Connection:

    id: str = ""

    source: str = ""

    target: str = ""

    name: str = ""