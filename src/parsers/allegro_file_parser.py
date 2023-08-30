from src.parsers.file_parser import FileParser, ParsedItem


class AllegroFileParser(FileParser):
    def __init__(self, file_handle, columns, section_identifier):
        super().__init__(file_handle, columns, section_identifier)


