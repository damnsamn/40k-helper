from classes import Model, Wargear
import helpers

# App state
is_active = True

# Parse models
models_csv = helpers.parse_csv("data/Datasheets_models.csv")
wargear_csv = helpers.parse_csv("data/Wargear_list.csv")

army = []
loaded_army = None

all_models = []
all_wargear = []


def add_model(*args, **kwargs):
    model = helpers.search_data(models_csv, *args, **kwargs)
    if(model):
        model = Model(model)
        army.append(model)
        print("Added model:", model.name)

def update_model(index, **kwargs):
    model = army[index]
    for key, value in kwargs.items():
        model[key] = value

def remove_model(index):
    model = army[index]
    if(model):
        army.pop(index)

def add_wargear(model_index, *args, **kwargs):
    model: Model = army[model_index]
    wargear = helpers.search_data(wargear_csv, *args, **kwargs)
    if(model and wargear):
        model.add_wargear(Wargear(wargear))