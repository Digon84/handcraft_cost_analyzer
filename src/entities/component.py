from dataclasses import dataclass


@dataclass
class Component:
    material: str
    component_type: str
    made_off: str
    shape: str
    color: str
    finishing_effect: str
    component_size: str
