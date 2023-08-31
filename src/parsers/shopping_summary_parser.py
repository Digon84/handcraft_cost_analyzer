import json
import re

from src.parsers.aliexpress_file_parser import AliexpressFileParser
from src.parsers.allegro_file_parser import AllegroFileParser


class ShoppingSummaryParser:
    def __init__(self):
        self.parsers_mapping = {"allegro": AllegroFileParser,
                                "ali_express": AliexpressFileParser}
        self.predefined_values = self.get_predefined_values()
        self.file_content = ""

    def parse_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            separator, shop = self.identify_file(f)
            if separator is not None and shop is not None:
                file_parser = self.parsers_mapping[shop](f, self.predefined_values, separator)
                file_parser.divide_into_sections()
                parsed_items = file_parser.parse_file()
                print("\n\nResults:")
                for row in parsed_items:
                    print("******")
                    for item in row:
                        print(item.column_name)
                        print(item.value)
                        print(item.parsed_ok)
                return parsed_items
            else:
                return None

    @staticmethod
    def identify_file(file_handle):
        identifiers_mapping = {r'dniowa dostawa': 'ali_express',
                               r'Szybka dostawa': 'ali_express',
                               'Zdjęcie przedmiotu': 'allegro'}

        file_content = file_handle.read()
        file_handle.seek(0)  # TODO: (double-read) reset the file cursor. Can it be handled in a different way?
        for regex, shop in identifiers_mapping.items():
            if re.search(regex, file_content):
                print(f'{file_handle.name} - {shop}')
                return regex, shop
            else:
                continue
        return None, None

    @staticmethod
    def get_predefined_values():
        # TODO: move hardcode to config file
        with open("G:\\Python\\handcraft_cost_analyzer\\assets\\predefined\\predefined_values.json",
                  'r', encoding='utf-8') as f:
            return json.loads(f.read())
