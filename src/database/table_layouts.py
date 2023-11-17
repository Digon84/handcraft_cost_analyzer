from dataclasses import dataclass


@dataclass
class Column:
    column_name: str
    is_mandatory: bool = True
    is_hidden: bool = False
    is_disabled: bool = False


INVENTORY_TABLE_LAYOUT = (
    Column(column_name="inventory_id", is_hidden=True),
    Column(column_name="Component_id", is_hidden=True),
    Column(column_name="material"),
    Column(column_name="type"),
    Column(column_name="made_off"),
    Column(column_name="shape"),
    Column(column_name="color"),
    Column(column_name="finishing_effect"),
    Column(column_name="component_size"),
    Column(column_name="amount"),
    Column(column_name="other", is_mandatory=False),
    Column(column_name="unit_price", is_mandatory=False, is_disabled=True),
    Column(column_name="total_price"),
    Column(column_name="add_date", is_mandatory=False, is_disabled=True),
)

COMPONENT_TABLE_LAYOUT = ()
COMPONENTS_USED_TABLE_LAYOUT = ()
PROJECT_TABLE_LAYOUT = ()
PRODUCT_TABLE_LAYOUT = ()
