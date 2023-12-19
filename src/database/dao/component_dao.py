from typing import List

from PyQt6.QtSql import QSqlQuery

from src.entities.component import Component


class ComponentDAO:
    def __init__(self):
        self.query = QSqlQuery()

    def insert_component(self, component: Component) -> (int, str):
        """
        Returns inserted component id or -1, error_message if query was not executed properly
        """
        self.query.prepare("INSERT INTO component(material, type, made_off, shape, color, finishing_effect,"
                           "component_size) VALUES(:material, :type, :made_off, :shape, :color,"
                           ":finishing_effect, :component_size)")

        self.bind_values(component)
        result = self.query.exec()

        if result:
            return self.query.result().lastInsertId(), ""
        else:
            return -1, self.query.lastError().text()

    def get_components(self) -> (list[Component], str):
        """
        Returns components from components table
        """
        self.query.prepare("SELECT * from component")

        result = self.query.exec()
        if result:
            components = []
            while self.query.next():
                row = {
                    "material": self.query.value(1),
                    "type": self.query.value(2),
                    "made_off": self.query.value(3),
                    "shape": self.query.value(4),
                    "color": self.query.value(5),
                    "finishing_effect": self.query.value(6),
                    "component_size": self.query.value(7)
                }
                components.append(Component(row))
            return components, ""
        else:
            return result, self.query.lastError().text()

    def get_component_id(self, component: Component) -> (int, str):
        """
        Returns component id or -1 if the entry with desired parameters does not exist.
        """
        self.query.prepare("SELECT * FROM component "
                           "WHERE material=:material AND type=:type AND made_off=:made_off "
                           "AND shape=:shape AND color=:color AND finishing_effect=:finishing_effect "
                           "AND component_size=:component_size")

        self.bind_values(component)
        result = self.query.exec()

        if self.query.next():
            return self.query.value("component_id"), ""
        else:
            return -1, self.query.lastError().text()

    def get_component_id_or_insert(self, component: Component):
        component_id, error_message = self.get_component_id(component)
        if component_id == -1:
            component_id, error_message = self.insert_component(component)

        if component_id == -1:
            error_message = self.query.lastError().text()

        return component_id, error_message

    def bind_values(self, component: Component):
        self.query.bindValue(":material", component.material)
        self.query.bindValue(":type", component.type)
        self.query.bindValue(":made_off", component.made_off)
        self.query.bindValue(":shape", component.shape)
        self.query.bindValue(":color", component.color)
        self.query.bindValue(":finishing_effect", component.finishing_effect)
        self.query.bindValue(":component_size", component.component_size)
