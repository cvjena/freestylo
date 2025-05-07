---
title: 'FreeStylo: An easy-to-use stylistic device detection tool for stylometry'

tags:
  - stylometry
  - stylistic devices
  - text analysis
  - text mining
  - text processing
  - text analysis
  - text analytics
  - text classification
  - text similarity
authors:
  - name: 'Felix Schneider'
    orcid: 0009-0008-9953-6695
    corresponding: true
    affiliation: 1
  - name: 'Joachim Denzler'
    orcid: 0000-0002-3193-3300
    affiliation: 1
affiliations:
  - name: Computer Vision Group, Friedrich-Schiller-Universität Jena
    index: 1
date: 27 October 2024
bibliography: paper.bib

---

# Summary

Stylistic devices are delibarately chosen linguistic expressions that
are used to convey a certain meaning or effect. They are often used in
literature to create a certain atmosphere or to convey a certain message.
Due to this matter, the detection of stylistic devices in text is an important
task in stylometry,the study of linguistic style. Often, finding these
stylistic devices is a tedious and costly process that involves close reading
of the texts, ideally by multiple experts. This is extra costly especially if
researchers aim to statistically analyze the usage of stylistic devices across
various texts.

To improve this state, this package provides an easy-to-use command-line
interface for detecting stylistic devices in text. The tool can be configured
with a simple configuration file. It is designed to be usable by both experts
and non-experts in programming. For those proficient in python, this package
also provides a library with a collection of classes to detect stylistic
devices in text, together with customizable text preprocessing (tokenizing,
POS-tagging, etc.).

The command-line tool is to be used on plain text files. It pre-processes the
text, detects the stylistic devices specified in the configuration file, and
writes the annotations to a JSON file. The classes contained in the library
can be used to work with the text in a more flexible way, e.g. by using
different pre-processing methods or already pre-processed text. The resulting
annotations can be saved in a JSON file or directly used as a data structure in
python. Additionally the library is easily extendable with your custom
stylistic device detectors.

# Statement of need

Stylotool is a package that provides a collection of approaches to detect
stylistic devices in text. While there exists a great variety of NLP libraries
like nltk [@nltk], spaCy [@spacy], or cltk [@cltk] and command-line tools like
CWB [@cwb], or UCS [@ucs] for the processing and low level analysis of text,
there is a lack of tools that are specifically designed for the detection of
stylistic devices.
Current options in this space would be for figurative language the online
tool Figurative Checker [@figurativechecker] or the MMFLD framework [@lai-etal-2023-multi],
which is a python framework. Other frameworks would be [@kuhn2024antithesis]
for the detection of antithesis, [@Li2023MetaphorDV] for the detection of
metaphors, [@schneider2021datadriven] for the detection of chiasmus,
or [@dubremetz2017chiasmus] for antimetabole detection.
Other tools are available for e.g. the detection of rhymes [@coles2019rhyme, @marozick2021rap].

However, most of those frameworks are not available as a ready-to-use tool, but as frameworks or code implementations of papers.
Also, many are only available for a specific language.
A commercial tool that was designed as a help for writers is the ProWritingAid [@prowritingaid2025], which seems to be able to find various features of texts. However, the whole extend of this tool is not visible from their information material.
Another commercial tool which is able to find stylistic devices such as animalification, similes, imagery, onomatopoeia, epizeuxis, and anadiplosis is the Literary Device Analyzer [@aussieai_literary_device_analyzer].

Besides the name similarity, this package is not related to the R stylo package [@eder2016stylor]. The R stylo package is a package for high level analysis of the writing style in a stylometric context, e.g. for authorship attribution. While the results of this package an also be used to compare the styles of different authors, the focus of this package is on the detection of stylistic devices in text.
The resulting detections can be used for various purposes, e.g. for the comparison of different text genres or time periods, or also for direct stylometry tasks like authorship attribution.

Information about the usage of stylistic devices is
important for many branches of stylometry, especially for the analysis of
literary texts. This package aims to fill this gap by providing an easy-to-use
tool and library for the detection of those stylistic devices. Due to its
simple and easily configurable command-line interface, the tool itself is
geared not only to people with programming knowledge, but also to literary
scholars that use distant reading methods in their research. Additionally it supports
multiple languages by design and is easy to extend to other languages. The software
contained in this package is designed to be used either as a library, usable in
other python programs, or as a stand-alone command-line tool.

# Design and Supported Stylistic Devices

The package contains a collection of approaches to detect stylistic devices
in text.
By default, the preprocessing is done by spaCy[@spacy] or cltk[@cltk].
Currently, the supported devices all work on a word level. They rely either
on supporting words, a word pair or multiple consecutive related words.
It would be possible to extend the package with other stylistic devices that
follow similar principles.
Additionally, the structure of the underlying framework is not restricted to
these kinds of devices. The same annotation method could be used to - for example -
mark scene boundaries and topic boundaries or changes in the tense of the text.
The following stylistic devices are currently supported:

## Chiasmus

This package includes the current state-of-the-art approach by
@schneider2021datadriven to detect chiasmi in text. A chiasmus is a rhetorical
device, that consists of two parallel phrases, where the second phrase is
a semantically related inversion of the first phrase. For example, the phrase
"Hard is the task, the samples are few" is a phrase that emphasizes the problem
of missing examples with the oppositional posing of the words "hard" and "few".

The chiasmus detector contained in this package has been trained using the
dataset published by @schneider2023hard. It works for English, German, and
Middle High German. It has been trained with word vectors provided by the
German 'de_core_news_lg' model by spaCy [@spacy]
However, since the model does not use the word vectors directly, but only their
cosine similarity, it can be used with any word vectors, as long as they
provide a vector for each token in the text.

The chiasmus detector needs some special lists to function properly.

- denylist: a list of Part of Speech (POS)-tags that are not allowed to be
  part of a chiasmus
- allowlist: a list of POS-tags that are allowed to be part of a chiasmus.
Be careful: if such a list is given, all other POS-tags are not allowed to
be part of a chiasmus.
- neglist: a list of negations in the target language.
- conjlist: a list of conjunctions in the target language.

For English, German, and Middle High German, defaults for the lists are provided in the package.
However, you can provide your own lists, if you want to use the chiasmus detector for a different language or if you want to use a different set of e.g. POS-tags.

## Metaphor

The metaphor detection approach in this package has specifically been developed for the low-resource language Middle High German, but can also be applied to more common high-resource language.
Specifically, adjective-noun metaphors like "thirsty car" are detected using a machine-learning based rating model.
The detector is based on the publication by @schneider2022metaphor.

Currently, the metaphor detector is available for English and Middle High German.
The word vectors are expected to be generated by the spaCy model 'en_core_web_lg' for English and
by the provided word vector FastText model for Middle High German.

## Alliteration and Alliterative Verse

The package further contains
a detector for both alliteration and alliterative verse. Alliteration comprise
phrases, where the initial letters of words are the same. Since alliteration is
a simple stylistic device, the detector is based on a simple rule-based
approach that orders all alliterations in the given text by the number of words
that are alliterated in the phrase. Additionally, the detector can also find
alliterative verses, which can contain some words additional in between the
words with the same initial letter. An example for alliterative verse would be
*"Pondering on the pending paper, I programmed the python package."* The user
can specify the maximum number of words that are allowed to be in between the
alliterated words, as well as words and POS-tags that do not count towards the
non-alliterated words. Since for example spaCy also tags punctuation and
newlines, the user can specify those to be excluded from the alliteration.

## Epiphora

An epiphora is a rhetorical device, that consists of multiple parallel phrases,
where the last word of each phrase is the same. For example, *"I thought of the
paper, I wrote the paper, I published the paper"* is an epiphora that
emphasizes the importance of the paper. The way this detector works is by
splitting the text into sentences, and then those sentences into phrases. The
detector searches for adjacent phrases that end with the same word. Those
phrase collections are then sorted by the number of phrases in the collection.

## Polysyndeton

A polysyndeton is a rhetorical device, that consists of multiple parallel
phrases, where each phrase is connected by a conjunction. For example, *"I
thought of the paper, and then I started writing it, and then I published it,
and then I received a lot of citations"* is a polysyndeton that, in a broader
context with a slower feel to it, emphasizes the the process of writing and
publishing a paper. The detector works by getting a list of all conjunctions,
or by getting the POS-tag of conjunctions, or by getting both, and then
splitting the text into sentences, and then counting the conjunctions in each
sentence, and then sorting the sentences by number of conjunctions.

# Usage

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

You can then run the tool using the following command:

```bash
stylotool --config config.json --input input.txt --output output.json
```

This will read the text from the file `input.txt`, preprocess (tokenize, POS-tag, etc.) the text, detect the stylistic devices specified in the configuration file, and write the results to the file `output.json`.

# Create your own detectors


The package is designed to be easily extendable with your own stylistic device detectors.
The `src` folder contains example scripts that show how you can retrain the models for the existing chiasmus and metaphor detectors.
You can also create your own stylistic device detectors by referring to the existing ones.
Especially the Alliteration Detector provides a very simple example that can be used as a template for your own detectors.
Please refer to the [Repository](https://github.com/cvjena/freestylo) of the package for more information on how to create your own detectors and contribute to the project.
If you create and want to contribute your own detecors, pull requests are very welcome!

# References
