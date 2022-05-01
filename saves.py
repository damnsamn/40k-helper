import re
import os
import json
from classes import Model, Wargear
import helpers
import state

saves_directory = ".saves/"
state_path = ".saves/.state"


def new_army():
    save_state("")
    state.army = []
    state.loaded_army = []
    print("Loaded army has been cleared successfully")


def save_army(name: str = None, verbose: bool = True):
    """save_army [name?]"""
    # Set filename
    if not name:
        filename = state.loaded_army or input("Name: ")
    else:
        filename = helpers.slugify(name) + ".json"
    full_path = saves_directory + filename

    # Create subdir if it doesn't already exist
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Does this file already exist? Prompt for overwrite
    if(os.path.exists(full_path)):
        overwrite = input(
            f"File {full_path} already exists.\nDo you want to overwrite? [Y/N]\n")
        if (overwrite == "n" or overwrite == "N"):
            return

    try:
        # Create file
        with open(full_path, "w") as file:
            ref_data = []
            for model in state.army:

                # Create a dict of only "datasheet_id" and "line" for later reference
                model_ref = {}
                model_ref["datasheet_id"] = model.datasheet_id
                model_ref["line"] = model.line

                # If the model has wargear, store the "wargear_id" and "line" of each
                if(model.wargear):
                    model_ref["wargear"] = []
                    for wargear in model.wargear:
                        model_ref["wargear"].append({
                            "wargear_id": wargear.wargear_id,
                            "line": wargear.line
                        })
                ref_data.append(model_ref)

            # Spit out ref_data as a string, formatted for JSON
            # Swap single-quotes for double-quotes
            json_string = re.sub(r"\'", "\"", format(ref_data))
            # Remove any whitespace
            json_string = re.sub(r"\s", "", json_string)

            # Save the file
            file.write(json_string)
            state.loaded_army = filename
            save_state(filename)
            if(verbose):
                print(f"Save successful: {full_path}")

    except Exception as e:
        print(format(e))


def load_army(filename: str):
    """load_army [name]"""
    # Format filename
    extension = re.search(r"\.\w+", filename)
    filename += "" if extension else ".json"

    with open(saves_directory + filename, 'r') as file:
        ref_data = json.load(file)

        # For each model in ref_data, get the Model and store it
        state.army = []
        for ref_model in ref_data:
            model = Model(helpers.search_data(
                state.models_csv,
                datasheet_id=ref_model["datasheet_id"],
                line=ref_model["line"]
            )[0])
            for ref_wg in ref_model.get("wargear", []):
                wg = Wargear(helpers.search_data(
                    state.wargear_csv,
                    wargear_id=ref_wg["wargear_id"],
                    line=ref_wg["line"]
                )[0])
                model.add_wargear(wg)
            state.army.append(model)

        # Overwrite current army
        state.loaded_army = filename
        save_state(filename)
        print("Load successful:", filename)


def save_state(data):
    with open(state_path, "w") as file:
        file.write(data)


def read_state():
    try:
        with open(state_path, "r") as file:
            return file.read()
    except:
        return None


def load_from_state():
    filename = read_state()
    if(filename):
        load_army(filename)