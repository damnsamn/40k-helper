import re
import os
import json
import helpers
import state

saves_directory = ".saves/"


def save_army(name: str, verbose: bool = True):
    # Set filename
    filename = helpers.slugify(name)
    filename = saves_directory + filename + ".json"

    # Create subdir if it doesn't already exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Does this file already exist? Prompt for overwrite
    if(os.path.exists(filename)):
        overwrite = input(
            f"File {filename} already exists.\nDo you want to overwrite? [Y/N]\n")
        if (overwrite == "n" or overwrite == "N"):
            return

    try:
        # Create file
        with open(filename, "w") as file:
            ref_data = []
            for model in state.army:

                # Create a dict of only "datasheet_id" and "line" for later reference
                model_ref = {}
                model_ref["datasheet_id"] = model.datasheet_id
                model_ref["line"] = model.line

                # If the model has wargear, store the "wargear_id" and "line" of each
                if(model.wargear):
                    model_ref.wargear = []
                    for wargear in model.wargear:
                        model_ref.wargear.append({
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
            if(verbose):
                print(f"Save successful: {filename}")

    except Exception as e:
        print(format(e))


def load_army(filename: str):
    # Format filename
    filename = helpers.slugify(filename)
    extension = re.search(r"\.\w+", filename)
    filename += "" if extension else ".json"

    try:
        # Open .json
        with open(saves_directory + filename, 'r') as file:
            ref_data = json.load(file)

            # For each model in ref_data, get the Model and store it
            temp_army = []
            for ref_model in ref_data:
                model = helpers.search_data( state.all_models,
                    datasheet_id=ref_model["datasheet_id"], line=ref_model["line"])
                temp_army.append(model)

            # Overwrite current army
            state.army = temp_army
            print("Load successful:", filename)

    except Exception as e:
        print(format(e))
