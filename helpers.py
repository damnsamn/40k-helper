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
    return int(re.search(r"\d+", string).group(0))


def search_data(iterable, name=None, **data):
    query = {}

    if(name):
        query["name"] = name

    for (key, value) in data.items():
        query[key] = value

    def filter_items(item):
        match = True
        for (key, value) in query.items():
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


class style:
    TAB = '\011'
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


    def str_format(CHAR, string):
        return CHAR + string + style.END

    def grey(string):
        return style.str_format(style.GREY, string)

    def red(string):
        return style.str_format(style.RED, string)

    def green(string):
        return style.str_format(style.GREEN, string)

    def yellow(string):
        return style.str_format(style.YELLOW, string)

    def blue(string):
        return style.str_format(style.BLUE, string)

    def magenta(string):
        return style.str_format(style.MAGENTA, string)

    def cyan(string):
        return style.str_format(style.CYAN, string)

    def bold(string):
        return style.str_format(style.BOLD, string)

    def underline(string):
        return style.str_format(style.UNDERLINE, string)


def strenth_toughness_check(strength, toughness):
    if strength/toughness >= 2:
        return 2
    elif strength/toughness <= 0.5:
        return 6
    elif strength > toughness:
        return 3
    elif strength < toughness:
        return 5
    else:
        return 4
