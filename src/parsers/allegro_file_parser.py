from src.parsers.file_parser import FileParser, ParsedItem
import re


class AllegroFileParser(FileParser):
    def __init__(self, file_handle, columns, section_identifier):
        super().__init__(file_handle, columns, section_identifier)

    def divide_into_sections(self):
        section = ""
        picture_match = False

        for line in self.file_handle.readlines():
            # When first match of the section_identifier skip first section
            if self.section_identifier in line and not picture_match:
                section = ""
                picture_match = True
            elif self.section_identifier in line:
                self.sections.append(section)
                section = ""
            section += line
        # Add the last section if any
        if section != "":
            self.sections.append(section)

    def get_price(self, section):
        reg = "([0-9]{1,4}) × ([0-9]{0,4},?[0-9]{0,4})"
        findall_result = set(re.findall(reg, section))

        if len(findall_result) == 1:
            prices = findall_result.pop()
            return float(prices[0]), float(prices[1].replace(',', '.'))
        else:
            return None, None
