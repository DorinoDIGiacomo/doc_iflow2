from dataclasses import dataclass


@dataclass
class ProcessExplanation:
    step_number: int
    component_type: str
    component_name: str

    title: str
    description: str

    icon: str