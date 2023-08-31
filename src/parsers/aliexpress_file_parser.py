import re

from src.parsers.file_parser import FileParser


class AliexpressFileParser(FileParser):
    def __init__(self, file_handle, columns, section_identifier):
        super().__init__(file_handle, columns, section_identifier)

    def get_price(self, section):
        reg = "([0-9]{0,4},?[0-9]{0,4})([0-9]{1,4}) × "
        findall_result = set(re.findall(reg, section))

        if len(findall_result) == 1:
            prices = findall_result.pop()
            return float(prices[0]), float(prices[1].replace(',', '.'))
        else:
            return None, None