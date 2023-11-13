import re
from dataclasses import dataclass, field
import datetime
from enum import Enum
from typing import List


class Parsed(Enum):
    OK = 0
    NOK = 1
    CONDITIONAL = 2


@dataclass
class ParsedItem:
    def __init__(self, column_name: str, value: str, parsed_ok: Parsed):
        self.column_name: str = column_name
        self.value: str = value
        self.parsed_ok: Parsed = parsed_ok


@dataclass
class Row:
    def __init__(self, hint: str):
        self.parsed_items: dict = {}
        self.hint = hint


class FileParser:
    # TODO: get rid of values_to_search_for and section_identifier??
    def __init__(self, file_handle, values_to_search_for=[], section_identifier=""):
        self.file_handle = file_handle
        self.values_to_search_for = values_to_search_for
        self.section_identifier = section_identifier
        self.sections = []

    def divide_into_sections(self):
        section = ""
        for line in self.file_handle.readlines():

            if self.section_identifier in line:
                self.sections.append(section)
                section = ""
            section += line
        # Add the last section if any
        if section != "":
            self.sections.append(section)

    def parse_file(self):
        parsed_items = []
        self.divide_into_sections()

        for section in self.sections:
            row = Row(hint="test")
            for column_name, values in self.values_to_search_for.items():
                search_result = re.search('|'.join([v.lower() for v in values]), section.lower())
                if search_result:
                    parsed_ok = Parsed.OK
                    parsed_value = search_result.group(0)
                else:
                    parsed_ok = Parsed.NOK
                    parsed_value = ""
                row.parsed_items[column_name] = ParsedItem(column_name=column_name, value=parsed_value,
                                                           parsed_ok=parsed_ok)

            size = self.parse_size(section)
            amount = self.parse_amount(section)
            unit_price = self.parse_unit_price(section)
            total_price = self.parse_total_price(section)

            row.parsed_items["size"] = ParsedItem(column_name="size", value=size,
                                                  parsed_ok=Parsed.OK if size != "" else Parsed.NOK)
            row.parsed_items["amount"] = ParsedItem(column_name="amount", value=amount,
                                                    parsed_ok=Parsed.OK if amount != "" else Parsed.NOK)
            row.parsed_items["unit_price"] = ParsedItem(column_name="unit_price", value=unit_price,
                                                        parsed_ok=Parsed.OK if unit_price != "" else Parsed.NOK)
            row.parsed_items["total_price"] = ParsedItem(column_name="total_price", value=total_price,
                                                         parsed_ok=Parsed.OK if total_price != "" else Parsed.NOK)
            row.parsed_items["add_date"] = ParsedItem(column_name="add_date", value=str(datetime.date.today()),
                                                      parsed_ok=Parsed.OK)
            row.hint = f"File: {self.file_handle.name} \n\nParsed section:\n{section}"
            self.apply_user_rules(row)

            parsed_items.append(row)
        return parsed_items

    @staticmethod
    def apply_user_rules(row: Row):
        mapping = [
            {"if": {"column": "type", "value": "TOHO"}, "then": {"column": "material", "value": "koralik"}},
            {"if": {"column": "type", "value": "miyuki"}, "then": {"column": "material", "value": "koralik"}},
            {"if": {"column": "type", "value": "japoński"}, "then": {"column": "material", "value": "koralik"}},
            {"if": {"column": "type", "value": "agat"}, "then": {"column": "made_off", "value": "kamień naturalny"}},
            {"if": {"column": "type", "value": "chryzokola"}, "then": {"column": "made_off", "value": "kamień naturalny"}},
            {"if": {"column": "type", "value": "lewa"}, "then": {"column": "made_off", "value": "kamień naturalny"}},
            {"if": {"column": "type", "value": "miyuki"}, "then": {"column": "made_off", "value": "szklane"}},
            {"if": {"column": "type", "value": "TOHO"}, "then": {"column": "made_off", "value": "szklane"}}
                   ]

        for user_map in mapping:
            if row.parsed_items[user_map["if"]["column"]].value.lower() == user_map["if"]["value"].lower():
                row.parsed_items[user_map["then"]["column"]].value = user_map["then"]["value"]
                row.parsed_items[user_map["then"]["column"]].parsed_ok = Parsed.CONDITIONAL


    @staticmethod
    def parse_size(section):
        regex_number_part = "([0-9]{0,4}[,.]?[0-9]{0,4})"
        regex_si_units = "(mm|ml) ?"
        reg = f"{regex_number_part} ?{regex_si_units}"
        result = set(re.findall(reg, section))

        if len(result) == 1:
            return ' '.join(result.pop())
        else:
            regex_size = "([0-9]{0,3}/[0-9]{1})"
            result = set(re.findall(regex_size, section))
            return result.pop() if len(result) == 1 else ""

    @staticmethod
    def parse_amount(section):
        regex_number_part = "([^/0-9-][0-9]{1,4})"
        regex_unit = "(szt|Szt|Pcs|pcs|Piece|piece)"
        reg = f"{regex_number_part} ?{regex_unit}"
        result = set(re.findall(reg, section))

        if len(result) == 1:
            return result.pop()[0].strip()
        else:
            # check if the values for all occurrences are the same
            if len(set([x.strip() for x, y in result])) == 1:
                return result.pop()[0].strip()
            else:
                return ""

    def get_price(self, section):
        raise NotImplementedError("Function get_price needs to be implemented before use.")

    def parse_unit_price(self, section):
        _, unit_price = self.get_price(section)
        return unit_price

    def parse_total_price(self, section):
        multiplier, unit_price = self.get_price(section)
        if multiplier != "" and unit_price != "":
            return multiplier * unit_price
        else:
            return ""
