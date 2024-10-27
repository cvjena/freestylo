import os
import logging
import json
import wget
import zipfile

model_list = [
        "chiasmus_de.pkl",
        "metaphor_de.torch",
        "fasttext_mgh.bin.zip",
        ]

model_base_url = "https://www.felixschneider.xyz/download/models/"

def get_model_path(model_to_load : str) -> str:
    if os.path.exists(model_to_load):
        return model_to_load

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

    model_path = config["model_path"]

    if not os.path.exists(model_path):
        os.makedirs(model_path, exist_ok=True)

    for model in model_list:
        if not os.path.exists(os.path.join(model_path, model)):
            logging.info(f"Downloading model {model} from {model_base_url}")
            wget.download(model_base_url+model, model_path)
            logging.info("done")
            if model.endswith(".zip"):
                with zipfile.ZipFile(os.path.join(model_path, model), 'r') as zip_ref:
                    zip_ref.extractall(model_path)


    model_to_load = os.path.join(model_path, model_to_load)
    if not os.path.exists(model_to_load):
        raise FileNotFoundError(f"Model {model_to_load} not found")
    return model_to_load





