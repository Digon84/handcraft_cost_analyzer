import re

from src.file_operations.parsers.file_parser import FileParser


class AliexpressFileParser(FileParser):
    def __init__(self, file_handle, columns, section_identifier):
        super().__init__(file_handle, columns, section_identifier)
        self.section_identifier = "złx"

    def divide_into_sections(self):
        section = ""
        for line in self.file_handle.readlines():
            section += line
            if self.section_identifier in line:
                self.sections.append(section)
                section = ""

    def get_price(self, section):
        reg = "([0-9]{0,4},?[0-9]{0,4})złx(.*)"
        findall_result = set(re.findall(reg, section))

        if len(findall_result) == 1:
            prices = findall_result.pop()
            return float(prices[1]), float(prices[0].replace(',', '.'))
        else:
            return "", ""
