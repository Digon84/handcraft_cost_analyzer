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

    def __init__(self, *product):
        self.product_id = product[0]
        self.project_id = product[1]
        self.product_name = product[2]
        self.amount = product[3]
        self.type = product[4]

        self.picture_1 = product[5] if len(product) >= 6 else None
        self.picture_2 = product[6] if len(product) >= 7 else None
        self.picture_3 = product[7] if len(product) >= 8 else None
