from classes import Model
import helpers

# App state
is_active = True

# Parse models
models_csv = helpers.parse_csv("data/Datasheets_models.csv")
wargear_csv = helpers.parse_csv("data/Datasheets_wargear.csv")

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
