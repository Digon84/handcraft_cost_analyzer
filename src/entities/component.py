from dataclasses import dataclass


@dataclass
class Component:
    material: str
    type: str
    made_off: str
    shape: str
    color: str
    finishing_effect: str
    component_size: str

    def __init__(self, row: dict):
        self.material = row["material"]
        self.type = row["type"]
        self.made_off = row["made_off"]
        self.shape = row["shape"]
        self.color = row["color"]
        self.finishing_effect = row["finishing_effect"]
        self.component_size = row["component_size"]
