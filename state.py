import helpers

# App state
is_active = True

# Parse models
models_csv = helpers.parse_csv("data/Datasheets_models.csv")
wargear_csv = helpers.parse_csv("data/Datasheets_wargear.csv")

army = []

all_models = []
all_wargear = []


def add_model(*args, **kwargs):
    model = helpers.search_data(all_models, *args, **kwargs)
    if(model):
        army.append(model)
        print("Added model:", model.name)

# def remove_model(ref):
    # Ref can be an index or a name
    # model = helpers.search_data(all_models, *args, **kwargs)
    # if(model):
    #     army.append(model)
    #     print("Added model:", model.name)
