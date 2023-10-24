from dataclasses import dataclass


@dataclass
class Project:
    project_id: int
    project_name: str
    fringles_table_name: str