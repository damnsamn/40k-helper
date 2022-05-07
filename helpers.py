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
        results = list(filter(filter_items, iterable))
        return results
    except StopIteration as e:
        print("Could not find item matching ", query)
    except Exception as e:
        print(format(e))


def search_data_partial(iterable, query: tuple):
    def filter_items(item):
        searchable = item[query[0]].lower()
        search = query[1]
        if (search in searchable):
            return True
        else:
            return False

    try:
        results = list(filter(filter_items, iterable))
        return results
    except StopIteration as e:
        print("Could not find any items partially matching ", query)
    except Exception as e:
        print(format(e))


class style:
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


class Table():
    def __init__(self, data: list[dict], heading: str = None, headers: list[str | tuple] = None, rename: dict = None, auto_index: bool = False):
        self.data = data
        for i, item in enumerate(self.data):
            item["index"] = i
        self.stringify_data()

        self.heading = heading
        self.headers = self.get_headers(headers, rename, auto_index)
        self.get_col_widths()

        self.chars = {
            "lt": "┌",
            "lm": "├",
            "lmd": "╞",
            "lb": "└",
            "rt": "┐",
            "rm": "┤",
            "rmd": "╡",
            "rb": "┘",
            "mt": "┬",
            "mmd": "╪",
            "mm": "┼",
            "mb": "┴",
            "h": "─",
            "hd": "═",
            "v": "│",
        }
        self.cell_padding_L = 1
        self.cell_padding_R = 1
        self.cell_padding_total = self.cell_padding_L + self.cell_padding_R

    def __getitem__(key):
        return Table[key]

    def stringify_data(self):
        for row in self.data:
            for key, value in row.items():
                row[key] = str(value)

    def get_headers(self, flat_list, rename, auto_index):
        # If we're not passed a list, create one based on the data
        if not flat_list:
            flat_list = []
            for row in self.data:
                for key, value in row.items():
                    if not key in flat_list and key != "index" and auto_index:
                        flat_list.append(key)

        header_list = []
        for value in flat_list:
            header_dict = {}
            if type(value) is (tuple or list):
                header_dict["key"] = value[0]
                header_dict["label"] = value[1]
            else:
                header_dict["key"] = value
                header_dict["label"] = rename[value] if rename and value in rename.keys(
                ) else value

            header_list.append(header_dict)

        return header_list

    def get_col_widths(self):
        # Initialise with header lengths
        for header in self.headers:
            header["width"] = len(header["label"])

        # Read each row, increase col_width if value is longer
        for row in self.data:
            for header in self.headers:
                if header["key"] in row.keys():
                    width = header["width"]
                    length = len(row[header["key"]])
                    if length > width:
                        header["width"] = length

    def print(self):
        self.print_heading()
        self.print_headers()
        self.print_separator("m", "d")
        for i, row in enumerate(self.data):
            self.print_line(row)
            self.print_separator("m" if i+1 < len(self.data) else "b")

    def print_heading(self):
        if self.heading:
            table_length = 1
            for header in self.headers:
                table_length += header["width"]
                table_length += self.cell_padding_total + 1

            print(style.bold(style.blue(self.chars["lt"] +
                  (self.chars["h"] * (len(self.heading) + 2)) +
                  self.chars["rt"])))
            print(style.bold(style.blue(
                self.chars["v"] + " " + self.heading + " " + self.chars["v"])))

        self.print_separator("t")

    def print_separator(self, y, style=""):
        h = self.chars["h" + style]
        l = self.chars["l" + y + style]
        m = self.chars["m" + y + style]
        r = self.chars["r" + y + style]

        row = l
        for i, header in enumerate(self.headers):
            row += h * (header["width"]+self.cell_padding_total)

            if i+1 < len(self.headers):
                row += m
            else:
                row += r
        print(row)

    def print_line(self, item):
        row = self.chars["v"]
        for header in self.headers:
            if header["key"] in item.keys():
                row += " " * (self.cell_padding_L)
                row += item[header["key"]]
                row += " " * \
                    (header["width"] - len(item[header["key"]]) +
                     self.cell_padding_R)
            else:
                row += " " * (header["width"] + self.cell_padding_total)
            row += self.chars["v"]
        print(row)

    def print_headers(self):
        row = self.chars["v"]
        for header in self.headers:
            row += " " * (self.cell_padding_L)
            row += style.magenta(style.bold(header["label"]))
            row += " " * (header["width"] -
                          len(header["label"]) + self.cell_padding_R)
            row += self.chars["v"]
        print(row)


def did_you_mean(search_term, iterable):
    original_search = search_term
    matches = []
    while len(search_term) and len(matches) < 5:
        search = search_data_partial(iterable, ("name", search_term))
        if len(search):
            for match in search:
                if len(matches) < 5 and match not in matches:
                    matches.append(match)
                else:
                    break
        search_term = search_term[0:-1]

    if len(matches) > 0:
        dym_table = Table(
            matches,
            "Did you mean?",
            [("index", ""), ("name", "Name"), "M", "WS", "BS", "S", "T", "W", "A", "Ld", "Sv"]
        )
        dym_table.print()
        print(style.magenta(f"Enter index, or nothing (TODO: Reword)"))
        user_input = input()

        if(len(user_input)):
            return matches[int(user_input)]
        else:
            return
    else:
        print("No matches found for", original_search)
