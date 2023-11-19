from csv import DictWriter


def write_content_to_csv(file_path, data_to_write):
    field_names = list(data_to_write[0].keys())
    with open(file_path, "w", encoding='utf-8') as f:
        writer = DictWriter(f, fieldnames=field_names, delimiter=";")
        for row in data_to_write:
            writer.writerow(row)
