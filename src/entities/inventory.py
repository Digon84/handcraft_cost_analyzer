from dataclasses import dataclass
import datetime

from src.entities.component import Component


@dataclass
class Inventory:
    amount: int
    other: str
    unit_price: float
    component: Component = None
    total_price: float = -1
    add_date: str = ""
    component_id: int = -1

    def __init__(self, row: dict, component: Component = None):
        self.amount = row["amount"]
        self.other = row["other"]
        self.unit_price = row["unit_price"]
        if component:
            self.component = component
        else:
            self.component = Component(row)
        self.total_price = row["total_price"]
        self.add_date = row["add_date"]
        self.component_id = row["component_id"] if "component_id" in row else -1
