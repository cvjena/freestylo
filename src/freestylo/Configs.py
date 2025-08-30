#    FreeStylo
#    A tool for the analysis of literary texts.
#    Copyright (C) 2024  Felix Schneider
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import json
import wget
import zipfile

model_list = [
        "chiasmus_de.pkl",
        "metaphor_de.torch",
        "metaphor_en.torch",
        "metaphor_mgh.torch",
        "fasttext_mgh.bin.zip",
        ]

model_base_url = "https://www.felixschneider.xyz/download/models/"

def get_config_dict():
    user_path = os.path.expanduser("~")
    config_path = os.path.join(user_path, ".config/freestylo/")
    config_file = os.path.join(config_path, "config.json")
    if not os.path.exists(config_file):
        os.makedirs(config_path, exist_ok=True)
        with open(config_file, "w") as f:
            json.dump(
                    {"model_path": os.path.join(user_path, ".freestylo/models/")},
                    f,
                    indent=4)

    with open(config_file, "r") as f:
        config = json.load(f)

    # read model_path environment variable
    if "FREESTYLO_MODEL_PATH" in os.environ:
        config["model_path"] = os.environ["FREESTYLO_MODEL_PATH"]

    return config

def get_model_path(model_to_load : str) -> str:
    if os.path.exists(model_to_load):
        print("found model locally")
        return model_to_load

    config = get_config_dict()

    model_path = config["model_path"]

    if not os.path.exists(model_path):
        os.makedirs(model_path, exist_ok=True)

    for model in model_list:
        if not os.path.exists(os.path.join(model_path, model)):
            print(f"Downloading model {model} from {model_base_url}")
            wget.download(model_base_url+model, model_path)
            print("done")
            if model.endswith(".zip"):
                with zipfile.ZipFile(os.path.join(model_path, model), 'r') as zip_ref:
                    zip_ref.extractall(model_path)


    model_to_load = os.path.join(model_path, model_to_load)
    if not os.path.exists(model_to_load):
        raise FileNotFoundError(f"Model {model_to_load} not found")
    return model_to_load





