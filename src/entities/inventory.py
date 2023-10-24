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

    def __post_init__(self):
        self.total_price = round(self.unit_price * self.amount, 3)
        self.add_date = str(datetime.date.today())
