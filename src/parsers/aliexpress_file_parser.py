from src.parsers.file_parser import FileParser


class AliexpressFileParser(FileParser):
    def __init__(self, file_handle, columns, section_identifier):
        super().__init__(file_handle, columns, section_identifier)
