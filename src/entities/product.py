from dataclasses import dataclass


@dataclass
class Product:
    product_id: int
    project_id: int
    product_name: str
    amount: int
    type: str
    picture_1: str
    picture_2: str
    picture_3: str
