import datetime
import json
import os
import re
from csv import DictReader

from src.file_operations.parsers.aliexpress_file_parser import AliexpressFileParser
from src.file_operations.parsers.allegro_file_parser import AllegroFileParser
from src.file_operations.parsers.file_parser import ParsedItem, Parsed


class ShoppingSummaryParser:
    def __init__(self):
        self.parsers_mapping = {"allegro": AllegroFileParser,
                                "ali_express": AliexpressFileParser}
        self.predefined_values = self.get_predefined_values()
        self.file_content = ""

    def parse_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            separator, shop = self.identify_file(f)
            if shop == "csv_file":
                parsed_items = []
                part_item = []
                dict_reader = DictReader(f, delimiter=";")
                for row in dict_reader:
                    for key, value in row.items():
                        part_item.append(ParsedItem(column_name=key,
                                                    value=value,
                                                    parsed_ok=Parsed.OK))
                    # Add current date
                    part_item.append(ParsedItem(column_name="add_date",
                                                value=str(datetime.date.today()),
                                                parsed_ok=Parsed.OK))
                    parsed_items.append(part_item)
                    part_item = []
                if parsed_items:
                    return parsed_items
                else:
                    return None
            if separator is not None and shop is not None:
                file_parser = self.parsers_mapping[shop](f, self.predefined_values, separator)
                parsed_items = file_parser.parse_file()
                return parsed_items
            else:
                return None

    @staticmethod
    def identify_file(file_handle):
        identifiers_mapping = {r'dniowa dostawa': 'ali_express',
                               r'Szybka dostawa': 'ali_express',
                               'Zdjęcie przedmiotu': 'allegro'}

        if "csv" in file_handle.name:
            return None, "csv_file"

        file_content = file_handle.read()

        file_handle.seek(0)  # TODO: (double-read) reset the file cursor. Can it be handled in a different way?
        for regex, shop in identifiers_mapping.items():
            if re.search(regex, file_content):
                return regex, shop
            else:
                continue
        return None, None

    @staticmethod
    def get_predefined_values():
        absolute_path = os.path.dirname(__file__)
        relative_path = "../../../assets/predefined/predefined_values.json"
        full_path = os.path.join(absolute_path, relative_path)
        with open(full_path,
                  'r', encoding='utf-8') as f:
            return json.loads(f.read())
