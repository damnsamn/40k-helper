import csv
import re

def parse_csv(path: str):
    csv_list = []
    with open(path, newline="", encoding='utf-8-sig') as csv_file:
        for row in csv.DictReader(csv_file, delimiter="|"):
            csv_list.append(row)
    return csv_list


def slugify(string: str):
    '''Remove dangerous characters for filenames or IDs\n
    Dashes and spaces become underscores. Any other non-word/digit character is removed'''
    slugified_string = string.strip().lower()
    slugified_string = re.sub(r"[\-\s]", "_", slugified_string)
    slugified_string = re.sub(r"[^\w\d_]", "", slugified_string)
    return slugified_string

def sanitise(string):
    return re.search(r"\d+", string)

def search_data(iterable, name=None, **data):
    query = {}

    if(name):
        query["name"] = name

    for (key, value) in data.items():
        query[key] = value

    def filter_items(item):
        match = True
        for (key,value) in query.items():
            if (item[key].lower() != query[key].lower()):
                match = False
        return match

    try:
        model = next(filter(filter_items, iterable))
        return model
    except StopIteration as e:
        print("Could not find model matching ", query)
    except Exception as e:
        print(format(e))

class colors:
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'