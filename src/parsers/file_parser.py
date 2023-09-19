import re
from dataclasses import dataclass


@dataclass
class ParsedItem:
    def __init__(self, column_name: str, value: str, parsed_ok: bool):
        self.column_name: str = column_name
        self.value: str = value
        self.parsed_ok: bool = parsed_ok


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
            items = []
            for column_name, values in self.values_to_search_for.items():
                search_result = re.search('|'.join([v for v in values]), section.lower())
                if search_result:
                    items.append(ParsedItem(column_name=column_name, value=search_result.group(0), parsed_ok=True))
                else:
                    items.append(ParsedItem(column_name=column_name, value="None", parsed_ok=False))

            size = self.parse_size(section)
            amount = self.parse_amount(section)
            unit_price = self.parse_unit_price(section)
            total_price = self.parse_total_price(section)

            items.append(ParsedItem(column_name="size", value=size, parsed_ok=size is not None))
            items.append(ParsedItem(column_name="amount", value=amount, parsed_ok=amount is not None))
            items.append(ParsedItem(column_name="unit_price", value=unit_price, parsed_ok=unit_price is not None))
            items.append(ParsedItem(column_name="total_price", value=total_price, parsed_ok=total_price is not None))

            parsed_items.append(tuple(items))
        return parsed_items

    @staticmethod
    def parse_size(section):
        regex_number_part = "([0-9]{0,4}[,.]?[0-9]{0,4})"
        regex_si_units = "(mm|ml)"
        reg = f"{regex_number_part} ?{regex_si_units}"
        result = set(re.findall(reg, section))

        if len(result) == 1:
            return ' '.join(result.pop())
        else:
            return None

    @staticmethod
    def parse_amount(section):
        regex_number_part = "([0-9]{0,4})"
        regex_unit = "(szt|pcs|piece)"
        reg = f"{regex_number_part} ?{regex_unit}"
        result = set(re.findall(reg, section))

        if len(result) == 1:
            return result.pop()[0]
        else:
            return None

    def get_price(self, section):
        raise NotImplementedError("Function get_price needs to be implemented before use.")

    def parse_unit_price(self, section):
        _, unit_price = self.get_price(section)
        return unit_price

    def parse_total_price(self, section):
        multiplier, unit_price = self.get_price(section)
        if multiplier is not None and unit_price is not None:
            return multiplier * unit_price
        else:
            return None
