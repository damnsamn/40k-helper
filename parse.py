import csv

def parse_csv(path: str):
    csv_list = []
    with open(path, newline="", encoding='utf-8-sig') as csv_file:
        for row in csv.DictReader(csv_file, delimiter="|"):
            csv_list.append(row)
    return csv_list


class ClassFactory:
    """Construct a new class with members matching the key-value pairs of the provided data"""
    def __init__(self, data:dict):
        for key, value in data.items():
            setattr(self, key, value)

model_csv = parse_csv("data/Datasheets_models.csv")
wargear_csv = parse_csv("data/Datasheets_wargear.csv")
