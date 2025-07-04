# FreeStylo - an easy-to-use stylistic device detection tool for stylometry

An easy-to-use package for detecting stylistic devices in text. This package is designed to be used in stylometry, the study of linguistic style.

For those proficient in python, this package provides a collection of approaches to detect stylistic devices in text. For those less proficient in python, this package provides a simple interface to detect stylistic devices in text with simple commands and user-friendly configuration.

# Installation

This package needs python 3.12 to run. It is recommended to create
a virtual environment for the package.
The package is available on PyPi and can be installed using pip.

```
pip install freestylo
```
# Usage Examples

## Standalone Tool

After installation, run the following command in the root of the repository:

```bash
freestylo --input test/documents/chiasmustext.txt \
    --output ./output.json \
    --config example_config.json
```

This creates the file `output.json` in the root of the repository, which contains the detected stylistic devices in the text file `test/documents/chiasmustext.txt`.
Afterwards, run the following command to get an overview over the results:

```bash
freestylo --mode report \
    --data output.json \
    --device chiasmus
```

The report mode is currently just implemented for Chiasmus.

The package can be used both as a library and as a stand-alone command-line tool.
Both from the library and from the command-line tool, the results can be saved in a JSON file.
This json file will contain the complete tokenized text.
When using the functions from the library, the result will be a python container with a similar structure to the JSON file.

The standalone version can be configured using a simple JSON configuration file. The file should specify the language of the text and the stylistic devices to detect. The following is an example configuration file:

```json
{
    "language": "de",
    "annotations": {
        "chiasmus": {
            "window_size": 30,
            "allowlist": ["NOUN", "VERB", "ADJ", "ADV"],
            "denylist": [],
            "model": "/chiasmus_de.pkl"
        }
    }
}
```

## Library

The library comprises a collection of functions to detect the stylistic devices, as well as preprocessing based on spaCy.
Should you want to use different preprocessing or use the package with a different language than the supported ones, a TextObject can be created and filled with the needed manually computed contents.
The stylistic device detectors can then be applied to the TextObject.

The `tests` folder contains a test for every stylistic device detector.
These tests show how to use the different detectors and how to create a TextObject.
All classes and functions are documented by docstrings.

A typical example code would look like this:
```python
from freestylo import TextObject as to
from freestylo import TextPreprocessor as tp
from freestylo import ChiasmusAnnotation as ca
from freestylo import MetaphorAnnotation as ma

# first, create a TextObject from the raw text
text = to.TextObject(
        textfile = "example_textfile.txt",
        language="en")

# create a TextPreprocessor object and process the text
# this does the tokenizing, lemmatizing, POS-tagging, etc.
preprocessor = tp.TextPreprocessor(language="en")
preprocessor.process_text(text)

# you can also use a different preprocessing of your choice
# without the TextPreprocessor object
# just fill the TextObject with the needed contents
# those could be provided e.g. by spaCy, nltk, cltk,
# or any other method of your choice

# many digital corpora are already tokenized and POS-tagged
# they may come in various formats, such as TEI XML, CoNLL, etc.
# if you have a text in those formats, you can fill the TextObject
# with the needed contents
# you can then fill the missing values in the TextObject
# with e.g. word vectors or other features created with a method of your choice.

# you can now add various annotations to the text object
# here, we add a chiasmus annotation
chiasmus = ca.ChiasmusAnnotation(
        text=text)
chiasmus.allowlist = ["NOUN", "VERB", "ADJ", "ADV"]
chiasmus.find_candidates()
chiasmus.load_classification_model("chiasmus_model.pkl")
chiasmus.score_candidates()

# here, we add a metaphor annotation
metaphor = ma.MetaphorAnnotation(
        text=text)
metaphor.find_candidates()
metaphor.load_model("metaphor_model.pkl")
metaphor.score_candidates()

# finally, save the annotated text to a json file
text.serialize("annotated_text.json")
```

The file `test/test_external_source.py` shows an an example of using the library without the text preprocessor. Instead the TextObject is filled by hand with the needed contents.

Currently supported stylistic devices are:
- Alliteration
- Chiasmus
- Epiphora
- Metaphor
- Polysyndeton

Please find an overview of the detectors and their methods in the [documentation](docs/docs.md).

## Create your own detectors!


The package is designed to be easily extendable with your own stylistic device detectors.
The `src` folder contains example scripts that show how you can retrain the models for the existing chiasmus and metaphor detectors.
You can also create your own stylistic device detectors by referring to the existing ones.
Especially the Alliteration Detector provides a very simple example that can be used as a template for your own detectors.
If you create and want to contribute your own detecors, pull requests are very welcome!


# Participation
The package is free and open-source software and contributions are very welcome.
It is designed to be a living project that is constantly improved and extended.
If you have implemented your own stylistic device detector, please consider contributing it to the package.
For details please refer to the [contribution guidelines](CONTRIBUTING.md).
Also, if you have any suggestions for improvements or if you find any bugs, please open an issue on the GitHub page.
