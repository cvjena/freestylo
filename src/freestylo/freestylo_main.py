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
import numpy as np

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
    parser.add_argument("--mode", help="Mode of operation", default="annotate", choices=["annotate", "report"])
    parser.add_argument("--input", help="Input text file. Used for annotate mode.", default="")
    parser.add_argument("--output", help="Output file. Used for annotate mode.", default="")
    parser.add_argument("--config", help="Configuration file. Used for annotate mode.", default="")
    parser.add_argument("--data", help="Data json file. Used for report mode.", default="")
    args = parser.parse_args()

    if args.mode == "annotate":
        annotate(args)
    elif args.mode == "report":
        report(args)

def report(args : argparse.Namespace):
    """
    This function is used to report the results of the analysis.
    It takes the data file and the device to report as arguments.
    """
    fail = False
    if args.data == "":
        print("Please specify a data file")
        fail = True
    if fail:
        print("Type freestylo --help for needed arguments")
        print("Exiting...")
        return

    report_chiasmus(args)
    report_metaphor(args)
    report_epiphora(args)
    report_alliteration(args)


def build_chiasmus_sentence(tokens, ids):
    """
    This function builds a chiasmus sentence from the tokens and ids.
    It takes the tokens and ids as arguments and returns the sentence as a list of strings.
    """
    return_list = []
    start_id = ids[0]
    end_id = ids[3]
    for i in range(start_id, end_id+1):
        if i in ids:
            return_list += ["<" + tokens[i] + "> "]
        else:
            return_list += [tokens[i]]
    return return_list

def report_chiasmus(args : argparse.Namespace):
    """
    This function reports the results of the chiasmus analysis.
    It takes the data file as an argument and prints the top chiasmus candidates.
    """

    with open(args.data) as f:
        data = json.load(f)

    tokens = data["tokens"]
    pos = data["pos"]

    chiasmus = data["annotations"]["chiasmus"]
    scores = [c["score"] for c in chiasmus]
    ids = [c["ids"] for c in chiasmus]

    index = np.argsort(scores)[::-1]

    max = min(10, len(scores))

    print("Top", max, "chiasmus candidates:")
    for i in range(max):
        score = scores[index[i]]
        ids_local = ids[index[i]]

        tokens_print = build_chiasmus_sentence(tokens, ids_local)
        pos_print = build_chiasmus_sentence(pos, ids_local)

        print("Score:", score, "ID:", ids_local)
        print_lines_aligned([tokens_print, pos_print])
        print()

def report_metaphor(args : argparse.Namespace):
    """
    This function reports the results of the metaphor analysis.
    It takes the data file as an argument and prints the top metaphor candidates.
    """

    with open(args.data) as f:
        data = json.load(f)
    tokens = data["tokens"]
    pos = data["pos"]
    metaphors = data["annotations"]["metaphor"]
    scores = [c["score"] for c in metaphors]
    ids = [c["ids"] for c in metaphors]
    index = np.argsort(scores)[::-1]
    max = min(10, len(scores))
    print("Top", max, "metaphor candidates:")
    for i in range(max):
        score = scores[index[i]]
        ids_local = ids[index[i]]

        tokens_print = [tokens[i] for i in ids_local]
        pos_print = [pos[i] for i in ids_local]

        print("Score:", score, "ID:", ids_local)
        print_lines_aligned([tokens_print, pos_print])
        print()


def report_epiphora(args : argparse.Namespace):
    """
    This function reports the results of the epiphora analysis.
    It takes the data file as an argument and prints the top epiphora candidates.
    """
    with open(args.data) as f:
        data = json.load(f)

    tokens = data["tokens"]
    pos = data["pos"]

    epiphora = data["annotations"]["epiphora"]
    scores = [c["score"] for c in epiphora]
    ids = [c["ids"] for c in epiphora]

    index = np.argsort(scores)[::-1]

    max = min(10, len(scores))

    print("Top", max, "epiphora candidates:")
    for i in range(max):
        score = scores[index[i]]
        ids_local = [ids[index[i]][0][0], ids[index[i]][-1][1]]

        tokens_print = [tokens[i] for i in range(ids_local[0], ids_local[1]+1)]
        pos_print = [pos[i] for i in range(ids_local[0], ids_local[1]+1)]

        print("Score:", score, "ID:", ids_local)
        print_lines_aligned([tokens_print, pos_print])
        print()

def report_alliteration(args : argparse.Namespace):
    """
    This function reports the results of the alliteration analysis.
    It takes the data file as an argument and prints the top alliteration candidates.
    """

    with open(args.data) as f:
        data = json.load(f)

    tokens = data["tokens"]
    pos = data["pos"]

    alliteration = data["annotations"]["alliteration"]
    scores = [c["score"] for c in alliteration]
    ids = [c["ids"] for c in alliteration]

    index = np.argsort(scores)[::-1]

    max = min(10, len(scores))

    print("Top", max, "alliteration candidates:")
    for i in range(max):
        score = scores[index[i]]
        ids_local = ids[index[i]]

        tokens_print = [tokens[i] for i in range(ids_local[0], ids_local[-1]+1)]
        pos_print = [pos[i] for i in range(ids_local[0], ids_local[-1]+1)]

        print("Score:", score, "ID:", ids_local)
        print_lines_aligned([tokens_print, pos_print])
        print()



def annotate(args : argparse.Namespace):
    """
    This function is used to annotate the input text with the specified annotations.
    It takes the input file, output file, and configuration file as arguments.
    It loads the text, preprocesses it, and adds the specified annotations.
    The results are then serialized to the output file.
    """
    fail = False
    if args.input == "":
        print("Please specify an input file")
        fail = True
    if args.output == "":
        print("Please specify an output file")
        fail = True
    if args.config == "":
        print("Please specify a configuration file")
        fail = True
    if fail:
        print("Type freestylo --help for needed arguments")
        print("Exiting...")
        return

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
            min_length = config["min_length"],
            ignore_tokens=config["ignore_tokens"])
    print("Finding candidates")
    alliteration.find_candidates()
    print("Done")


def get_longest_string(lines, index):
    """
    This function returns the longest string in a list of strings at a given index.
    """
    longest_string = 0
    for line in lines:
        if len(line[index]) > longest_string:
            longest_string = len(line[index])
    return longest_string


def print_lines_aligned(lines):
    """
    This function prints a list of strings in a aligned format.
    """
    num_lines = len(lines)
    num_tokens = len(lines[0])

    print_strings = ["" for _ in lines]

    for t in range(num_tokens):
        max_length = get_longest_string(lines, t) + 1
        for l in range(num_lines):
            string = lines[l][t].replace("\n", "")
            string += " " * (max_length - len(string))
            print_strings[l] += string

    for ps in print_strings:
        print(ps)








if __name__ == '__main__':
    main()
