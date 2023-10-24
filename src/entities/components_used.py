from dataclasses import dataclass


@dataclass
class ComponentsUsed:
    project_id: int
    component_id: int
    amount: int
    unit_price: float
    total_price: float = 0.0

    def __post_init__(self):
        self.total_price = round(self.amount * self.unit_price, 3)
