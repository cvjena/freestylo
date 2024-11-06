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

import argparse
import json
import freestylo.ChiasmusAnnotation as ca
import freestylo.MetaphorAnnotation as ma
import freestylo.EpiphoraAnnotation as ea
import freestylo.PolysyndetonAnnotation as pa
import freestylo.AlliterationAnnotation as aa
import freestylo.TextObject as to
import freestylo.TextPreprocessor as tp

def main():
    """
    This is the main function of the freestylo tool.
    When you run the tool from the command line, this function is called.
    It reads the input text, preprocesses it, and adds the specified annotations.
    The results are then serialized to a file.
    """
    parser = argparse.ArgumentParser(description="Stylometric analysis tool")
    parser.add_argument("--input", help="Input text file")
    parser.add_argument("--output", help="Output file")
    parser.add_argument("--config", help="Configuration file")
    args = parser.parse_args()

    print("Loading text from", args.input)
    print("Loading configuration from", args.config)
    print("Saving results to", args.output)

    print("Loading config...")
    # load config
    with open(args.config) as f:
        config = json.load(f)
    print("Done")

    max_length = None
    if "nlp_max_length" in config:
        max_length = config["nlp_max_length"]



    # Load text

    print("Loading text...")
    text = to.TextObject(
            textfile = args.input,
            language=config["language"])
    print("Done")

    # Preprocess text
    print("Preprocessing text...")
    preprocessor = tp.TextPreprocessor(language=config["language"], max_length=max_length)
    preprocessor.process_text(text)
    print("Done")
    # Annotate
    annotation_dict = config["annotations"]
    for annotation in annotation_dict:
        if annotation == "chiasmus":
            add_chiasmus_annotation(text, annotation_dict[annotation])
        elif annotation == "metaphor":
            add_metaphor_annotation(text, annotation_dict[annotation])
        elif annotation == "epiphora":
            add_epiphora_annotation(text, annotation_dict[annotation])
        elif annotation == "polysyndeton":
            add_polysyndeton_annotation(text, annotation_dict[annotation])
        elif annotation == "alliteration":
            add_alliteration_annotation(text, annotation_dict[annotation])
        text.serialize(args.output)
    print("Added all annotations")

    # Serialize results
    print("Serializing results")
    text.serialize(args.output)
    print("Done")


    print("Finished")

def add_chiasmus_annotation(text, config):
    """
    This function adds chiasmus annotations to the text.
    """
    print("Adding chiasmus annotation")
    chiasmus = ca.ChiasmusAnnotation(
            text=text,
            window_size = config["window_size"])
    chiasmus.allowlist = config["allowlist"]
    chiasmus.denylist = config["denylist"]
    print("Finding candidates")
    chiasmus.find_candidates()
    print("Loading model")
    chiasmus.load_classification_model(config["model"])
    print("Scoring candidates")
    chiasmus.score_candidates()
    print("Done")

def add_metaphor_annotation(text, config):
    """
    This function adds metaphor annotations to the text.
    """
    print("Adding metaphor annotation")
    metaphor = ma.MetaphorAnnotation(text)
    print("Finding candidates")
    metaphor.find_candidates()
    print("Loading model")
    metaphor.load_model(config["model"])
    print("Scoring candidates")
    metaphor.score_candidates()
    print("Done")

def add_epiphora_annotation(text, config):
    """
    This function adds epiphora annotations to the text.
    """
    print("Adding epiphora annotation")
    epiphora = ea.EpiphoraAnnotation(
            text = text,
            min_length = config["min_length"],
            conj = config["conj"],
            punct_pos = config["punct_pos"])
    print("Finding candidates")
    epiphora.find_candidates()
    print("Done")

def add_polysyndeton_annotation(text, config):
    """
    This function adds polysyndeton annotations to the text.
    """
    print("Adding polysyndeton annotation")
    polysyndeton = pa.PolysyndetonAnnotation(
            text = text,
            min_length = config["min_length"],
            conj = config["conj"],
            sentence_end_tokens = config["sentence_end_tokens"])
    print("Finding candidates")
    polysyndeton.find_candidates()
    print("Done")

def add_alliteration_annotation(text, config):
    """
    This function adds alliteration annotations to the text.
    """
    print("Adding alliteration annotation")
    alliteration = aa.AlliterationAnnotation(
            text = text,
            max_skip = config["max_skip"],
            min_length = config["min_length"])
    print("Finding candidates")
    alliteration.find_candidates()
    print("Done")

if __name__ == '__main__':
    main()
