import parse

# App state
is_active = True

# Parse models
models_csv = parse.parse_csv("data/Datasheets_models.csv")
wargear_csv = parse.parse_csv("data/Datasheets_wargear.csv")

army = []

model_list = []
wargear_list = []


def get_model(name=None, **data):
    query = {}
    datasheet_id = None
    line = None

    for (key, value) in data.items():
        match key:
            case "name":
                name = value
            case "id":
                datasheet_id = value
            case "line":
                line = value

    if(name):
        query["name"] = name
    if(datasheet_id):
        query["datasheet_id"] = datasheet_id
    if(line):
        query["line"] = line


    def search_models(item):
        return (
            item.name == name or
            (item.datasheet_id == datasheet_id and item.line == line)
        )

    try:
        model = next(filter(search_models, model_list))
        return model
    except Exception:
        print("Could not find model matching ", query)
