# FreeStylo Documentation

An easy-to-use package for detecting **stylistic devices** in text. Designed for use in **stylometry**, the study of linguistic style.

This document provides a complete reference to FreeStylo, including installation, usage as a CLI tool and as a Python library, and detailed documentation for each class.

# Installation

FreeStylo requires **Python 3.12**.

Install from PyPI:

```bash
pip install freestylo
```

It is recommended to install into a virtual environment.

---

# Configuration

The package can be configured using the configuration file under `~/.config/freestylo/config.json`. This file will be created when the tool is first run or the library needs information from the config file.
Currently only the model download location can be configured.
The model path can also be overridden by setting the environment variable `FREESTYLO_MODEL_PATH`.

The default configuration is:
```json
{
    "model_path": "~/.freestylo/models/"
}
```

---

# Command Line Interface (CLI)

### Annotate Mode

Annotates a text with stylistic devices:

```bash
freestylo --mode annotate \
    --input input.txt \
    --output output.json \
    --config config.json
```

### Report Mode

Reports the results of annotations:

```bash
freestylo --mode report --data output.json
```

Currently reports for **Chiasmus**, **Metaphor**, **Epiphora**, and **Alliteration** are supported.

### Example Config File

```json
{
  "language": "de",
  "annotations": {
    "chiasmus": {
      "window_size": 30,
      "allowlist": ["NOUN", "VERB", "ADJ", "ADV"],
      "denylist": [],
      "model": "chiasmus_de.pkl"
    },
    "metaphor": {
      "model": "metaphor_de.torch"
    },
    "epiphora": {
      "min_length": 2,
      "conj": ["und", "oder", "aber", "noch"],
      "punct_pos": "PUNCT"
    }
  }
}
```

---

# Library Usage

Example usage as a Python library:

```python
from freestylo import TextObject, TextPreprocessor
from freestylo import ChiasmusAnnotation, MetaphorAnnotation

# Create a TextObject
text = TextObject(text="This is an example text.", language="en")

# Preprocess the text
pre = TextPreprocessor(language="en")
pre.process_text(text)

# Run detectors
chiasmus = ChiasmusAnnotation(text)
chiasmus.allowlist = ["NOUN", "VERB", "ADJ", "ADV"]
chiasmus.find_candidates()
chiasmus.load_classification_model("chiasmus_de.pkl")
chiasmus.score_candidates()

# Serialize results
text.serialize("output.json")
```

---

# Core Classes

## TextObject

**Purpose:** Represents a text and its linguistic annotations.

### Member Variables

* `textfile`: path to file (str, optional)
* `text`: raw text (str)
* `language`: language code (str)
* `tokens`: list of tokens
* `pos`: list of POS tags
* `lemmas`: list of lemmas
* `dep`: list of dependency relations
* `vectors`: list of word vectors
* `annotations`: list of annotations (detector objects)
* `token_offsets`: list of (start, end) positions for tokens

### Functions

* `save_as(filename)`: Save as pickle.
* `serialize(filename)`: Save as JSON.
* `has_text()`: Check if text exists.
* `has_tokens()`, `has_pos()`, `has_lemmas()`, `has_dep()`, `has_vectors()`, `has_annotations()`: Availability checks.

---

## TextPreprocessor

**Purpose:** Preprocesses text using spaCy or Middle High German pipeline.

### Member Variables

* `nlp`: the loaded spaCy pipeline or `MGHPreprocessor`

### Functions

* `process_text(text: TextObject)`: fills the TextObject with tokens, POS, lemmas, dependencies, vectors, token offsets.

---

## MGHPreprocessor

**Purpose:** Preprocessor for Middle High German texts using CLTK and FastText.

### Functions

* `__call__(text: str) -> list[MGHToken]`: tokenizes and annotates MHG text.
* `get_next_word(text, idx)`: helper to get next word.

### MGHToken

Represents one Middle High German token.

* `text`, `pos`, `lemma`, `dep`, `vector`, `idx`

---

# Stylistic Device Detectors

Each detector appends itself to the `TextObject.annotations` and provides candidates.

---

## ChiasmusAnnotation

**Purpose:** Detects **Chiasmus** patterns (ABBA structures).

### Member Variables

* `text`: TextObject
* `window_size`: size of search window (default 30)
* `candidates`: list of ChiasmusCandidate
* `allowlist`, `denylist`, `neglist`, `poslist`, `conjlist`: POS filters
* `model`: classification model (sklearn SVM)
* `type`: "chiasmus"

### Functions

* `find_candidates()`: identifies ABBA candidates.
* `load_classification_model(path)`: loads classification model (pickle).
* `score_candidates()`: scores candidates with model.
* `serialize()`: serialize candidates.
* `get_features(candidate)`: extract feature vector.
* `get_dubremetz_features`, `get_lexical_features`, `get_semantic_features`: feature extraction helpers.

### Additional Info

* **Model required**: yes (SVM, `chiasmus_de.pkl`).
* **Language**: works for all languages, though the included model is trained on German.

---

## MetaphorAnnotation

**Purpose:** Detects **Metaphors** by adjective–noun pairs.

### Member Variables

* `text`: TextObject
* `candidates`: list of MetaphorCandidate
* `device`: torch device (CPU/GPU)
* `type`: "metaphor"
* `model`: PyTorch model

### Functions

* `find_candidates()`: finds ADJ–NOUN pairs.
* `serialize()`: serialize candidates.
* `load_model(path)`: loads PyTorch model.
* `get_vectors()`: returns adj/noun vectors.
* `score_candidates()`: assigns scores.

### Additional Info

* **Model required**: yes (`metaphor_de.torch`, `metaphor_mgh.torch`).
* **Languages supported**: German (`de`), Middle High German (`mgh`).

---

## EpiphoraAnnotation

**Purpose:** Detects **Epiphora** (repetition at phrase endings).

### Member Variables

* `text`: TextObject
* `type`: "epiphora"
* `candidates`: list of EpiphoraCandidate
* `min_length`: minimum repeated phrases
* `conj`: conjunctions for splitting
* `punct_pos`: POS tag for punctuation

### Functions

* `split_in_phrases()`: segment text.
* `find_candidates()`: detect repetitions.
* `serialize()`: serialize candidates.

### EpiphoraCandidate

* `ids`: list of phrases
* `word`: repeated word
* `score`: number of repetitions

### Additional Info

* **Model required**: no.
* **Languages supported**: all.

---

## PolysyndetonAnnotation

**Purpose:** Detects **Polysyndeton** (excessive conjunction use).

### Member Variables

* `text`: TextObject
* `type`: "polysyndeton"
* `candidates`: list of PolysyndetonCandidate
* `min_length`: minimum length
* `conj`: conjunction list
* `sentence_end_tokens`: sentence delimiters
* `punct_pos`: POS for punctuation

### Functions

* `split_in_phrases()`: segment into phrases.
* `find_candidates()`: detect polysyndeton.
* `check_add_candidate()`: helper.
* `serialize()`: serialize candidates.

### PolysyndetonCandidate

* `ids`: phrase indices
* `word`: repeated word
* `score`: number of repetitions

### Additional Info

* **Model required**: no.
* **Languages supported**: all.

---

## AlliterationAnnotation

**Purpose:** Detects **Alliteration** (repetition of initial sounds/letters).

### Member Variables

* `text`: TextObject
* `type`: "alliteration"
* `candidates`: list of AlliterationCandidate
* `max_skip`: allowed distance between hits
* `min_length`: minimum sequence length
* `skip_tokens`: tokens to skip
* `ignore_tokens`: tokens to ignore

### Functions

* `find_candidates()`: detect alliterations.
* `serialize()`: serialize candidates.

### AlliterationCandidate

* `ids`: token indices
* `char`: repeated character
* `score`: length of sequence

### Additional Info

* **Model required**: no.
* **Languages supported**: all.

---

# Models and Languages

Some detectors require pre-trained models. Models are downloaded automatically to `~/.freestylo/models/` if not found.

| Detector     | Model Required? | Model File(s)                             | Supported Languages        |
| ------------ | --------------- | ----------------------------------------- | -------------------------- |
| Chiasmus     | Yes             | `chiasmus_de.pkl`                         | All (trained on German)    |
| Metaphor     | Yes             | `metaphor_de.torch`, `metaphor_mgh.torch` | German, Middle High German |
| Epiphora     | No              | –                                         | All                        |
| Polysyndeton | No              | –                                         | All                        |
| Alliteration | No              | –                                         | All                        |

> **Note:** *"Model Required?"* means whether a detector needs a trained ML model to function. If no, the detector is rule-based.

---

# Extending FreeStylo

You can create new detectors by following the pattern of existing ones:

* Subclass-like class with `find_candidates()` and `serialize()`.
* Append to `TextObject.annotations`.
* For ML-based detectors, integrate model loading with `Configs.get_model_path()`.

Contributions of new detectors are welcome (see `CONTRIBUTING.md`).
