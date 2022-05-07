from classes import Model, Wargear
from helpers import search_data, Table, parse_csv, did_you_mean, style

# App state
is_active = True

# Parse models
models_csv = parse_csv("data/Datasheets_models.csv")
wargear_csv = parse_csv("data/Wargear_list.csv")
damage_profiles_csv = parse_csv("data/Datasheets_damage.csv")

army = []
loaded_army = None

all_models = []
all_wargear = []

def add_model(*args, **kwargs):
    model = search_data(models_csv, *args, **kwargs)
    if(len(model)):
        model = Model(model[0])
        army.append(model)
        print("Added model:", model.name)
    elif len(args) == 1: # If only a name was provided
        name = args[0]
        correction = did_you_mean(name, models_csv)
        if(correction):
            model = Model(correction)
            army.append(model)
            print("Added model:", model.name)



def update_model(index, **kwargs):
    model = army[index]
    for key, value in kwargs.items():
        model[key] = value

def remove_model(index):
    model = army[index]
    if(model):
        print("Removed model:", model.name)
        army.pop(index)

def add_wargear(model_index, *args, **kwargs):
    model: Model = army[model_index]
    wargear = search_data(wargear_csv, *args, **kwargs)
    if model:
        if len(wargear):
            wargear = Wargear(wargear[0])
            model.add_wargear(wargear)
            print(f"Added wargear {style.bold(wargear.name)} to model {style.bold(model.name)}")
        elif len(args) == 1: # If only a name was provided
            name = args[0]
            correction = did_you_mean(name, wargear_csv)
            if(correction):
                wargear = Wargear(correction)
                model.add_wargear(wargear)
                print(f"Added wargear {style.bold(wargear.name)} to model {style.bold(model.name)}")

def remove_wargear(model_index, wargear_index):
    model = army[model_index]
    if(model):
        print("Removed wargear:", model.wargear[wargear_index].name, "from model:", model.name)
        model.remove_wargear(wargear_index)

