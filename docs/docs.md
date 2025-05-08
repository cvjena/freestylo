<a id="freestylo"></a>

# freestylo

<a id="freestylo.EpiphoraAnnotation"></a>

# freestylo.EpiphoraAnnotation

<a id="freestylo.EpiphoraAnnotation.EpiphoraAnnotation"></a>

## EpiphoraAnnotation Objects

```python
class EpiphoraAnnotation()
```

This class is used to find epiphora candidates in a text.
It uses the TextObject class to store the text and its annotations.

<a id="freestylo.EpiphoraAnnotation.EpiphoraAnnotation.__init__"></a>

#### \_\_init\_\_

```python
def __init__(text: TextObject,
             min_length=2,
             conj=["and", "or", "but", "nor"],
             punct_pos="PUNCT")
```

Constructor for the EpiphoraAnnotation class.

Parameters
----------
text : TextObject
    The text to be analyzed.
min_length : int, optional
    The minimum length of the epiphora candidates.
conj : list, optional
    A list of conjunctions that should be considered when looking for epiphora.
punct_pos : str, optional
    The part of speech tag for punctuation.

<a id="freestylo.EpiphoraAnnotation.EpiphoraAnnotation.split_in_phrases"></a>

#### split\_in\_phrases

```python
def split_in_phrases()
```

This method splits the text into phrases.

Returns
-------
list
    A list of lists, each containing the start and end index of a phrase.

<a id="freestylo.EpiphoraAnnotation.EpiphoraAnnotation.find_candidates"></a>

#### find\_candidates

```python
def find_candidates()
```

This method finds epiphora candidates in the text.

<a id="freestylo.EpiphoraAnnotation.EpiphoraAnnotation.serialize"></a>

#### serialize

```python
def serialize() -> list
```

This method serializes the epiphora candidates.

Returns
-------
list
    A list of dictionaries, each containing the ids, length, and word of an epiphora candidate.

<a id="freestylo.EpiphoraAnnotation.EpiphoraCandidate"></a>

## EpiphoraCandidate Objects

```python
class EpiphoraCandidate()
```

This class represents an epiphora candidate.

<a id="freestylo.EpiphoraAnnotation.EpiphoraCandidate.__init__"></a>

#### \_\_init\_\_

```python
def __init__(ids, word)
```

Constructor for the EpiphoraCandidate class.

Parameters
----------
ids : list
    A list of token ids that form the candidate.
word : str
    The word that the candidate ends with.

<a id="freestylo.EpiphoraAnnotation.EpiphoraCandidate.score"></a>

#### score

```python
@property
def score()
```

This property returns the score of the candidate.

<a id="freestylo.TextObject"></a>

# freestylo.TextObject

<a id="freestylo.TextObject.TextObject"></a>

## TextObject Objects

```python
class TextObject()
```

This class is used to store a text and its annotations.

<a id="freestylo.TextObject.TextObject.__init__"></a>

#### \_\_init\_\_

```python
def __init__(textfile=None, text=None, language='')
```

Constructor for the TextObject class.

Parameters
----------
textfile : str, optional
    The path to a text file.
text : str, optional

language : str, optional
    The language of the text.

<a id="freestylo.TextObject.TextObject.save_as"></a>

#### save\_as

```python
def save_as(filename)
```

This method saves the TextObject as a pickle file.

Parameters
----------
filename : str

<a id="freestylo.TextObject.TextObject.serialize"></a>

#### serialize

```python
def serialize(filename)
```

This method serializes the TextObject as a JSON file.

Parameters
----------
filename : str

<a id="freestylo.TextObject.TextObject.has_text"></a>

#### has\_text

```python
def has_text()
```

This method checks if the TextObject has a text.

<a id="freestylo.TextObject.TextObject.has_tokens"></a>

#### has\_tokens

```python
def has_tokens()
```

This method checks if the TextObject has tokens.

<a id="freestylo.TextObject.TextObject.has_pos"></a>

#### has\_pos

```python
def has_pos()
```

This method checks if the TextObject has part-of-speech tags.

<a id="freestylo.TextObject.TextObject.has_lemmas"></a>

#### has\_lemmas

```python
def has_lemmas()
```

This method checks if the TextObject has lemmas.

<a id="freestylo.TextObject.TextObject.has_dep"></a>

#### has\_dep

```python
def has_dep()
```

This method checks if the TextObject has dependency relations.

<a id="freestylo.TextObject.TextObject.has_vectors"></a>

#### has\_vectors

```python
def has_vectors()
```

This method checks if the TextObject has vectors.

<a id="freestylo.TextObject.TextObject.has_annotations"></a>

#### has\_annotations

```python
def has_annotations()
```

This method checks if the TextObject has annotations.

<a id="freestylo.MGHPreprocessor"></a>

# freestylo.MGHPreprocessor

<a id="freestylo.MGHPreprocessor.MGHPreprocessor"></a>

## MGHPreprocessor Objects

```python
class MGHPreprocessor()
```

This class preprocesses Middle High German text.

<a id="freestylo.MGHPreprocessor.MGHPreprocessor.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Constructor for the MGHPreprocessor class.

<a id="freestylo.MGHPreprocessor.MGHPreprocessor.__call__"></a>

#### \_\_call\_\_

```python
def __call__(text)
```

This method preprocesses Middle High German text.

Parameters
----------
text : str
    The text to be preprocessed.

Returns
-------
list
    A list of MGH tokens.

<a id="freestylo.MGHPreprocessor.MGHPreprocessor.get_next_word"></a>

#### get\_next\_word

```python
def get_next_word(text, idx)
```

This method finds the next word in a text.

Parameters
----------
text : list[str]
    The text to be searched.
idx : int
    The index of the current word.

Returns
-------
str
    The next word in the text.
int
    The index of the next word.

<a id="freestylo.MGHPreprocessor.MGHToken"></a>

## MGHToken Objects

```python
class MGHToken()
```

This class represents a Middle High German token.

<a id="freestylo.MGHPreprocessor.MGHToken.__init__"></a>

#### \_\_init\_\_

```python
def __init__(text, pos, lemma, dep, vector, idx)
```

Constructor for the MGHToken class.

Parameters
----------
text : str
    The text of the token.
pos : str
    The part of speech of the token.
lemma : str
    The lemma of the token.
dep : str
    The dependency of the token.
vector : np.array
    The vector representation of the token.
idx : int
    The index of the token in the text.

<a id="freestylo.AlliterationAnnotation"></a>

# freestylo.AlliterationAnnotation

<a id="freestylo.AlliterationAnnotation.AlliterationAnnotation"></a>

## AlliterationAnnotation Objects

```python
class AlliterationAnnotation()
```

This class is used to find alliterations candidates in a text.
It uses the TextObject class to store the text and its annotations.

<a id="freestylo.AlliterationAnnotation.AlliterationAnnotation.__init__"></a>

#### \_\_init\_\_

```python
def __init__(text: TextObject,
             max_skip=2,
             min_length=3,
             skip_tokens=[
                 ".", ",", ":", ";", "!", "?", "…", "(", ")", "[", "]", "{",
                 "}", "„", "“", "‚", "‘:", "‘", "’"
             ],
             ignore_tokens=None)
```

Parameters
----------
text : TextObject
    The text to be analyzed.
max_skip : int, optional
min_length : int, optional
skip_tokens : list, optional
    A list of tokens that should be skipped when looking for alliterations.

<a id="freestylo.AlliterationAnnotation.AlliterationAnnotation.find_candidates"></a>

#### find\_candidates

```python
def find_candidates()
```

This method finds alliteration candidates in the text.

<a id="freestylo.AlliterationAnnotation.AlliterationAnnotation.serialize"></a>

#### serialize

```python
def serialize() -> list
```

This method serializes the alliteration candidates into a list of dictionaries.

Returns
-------
list
    A list of dictionaries containing the ids, length and character of the alliteration candidates.

<a id="freestylo.AlliterationAnnotation.AlliterationCandidate"></a>

## AlliterationCandidate Objects

```python
class AlliterationCandidate()
```

This class represents an alliteration candidate.

<a id="freestylo.AlliterationAnnotation.AlliterationCandidate.__init__"></a>

#### \_\_init\_\_

```python
def __init__(ids, char)
```

Parameters
----------
ids : list
    A list of token ids that form the alliteration candidate.
char : str
    The character that the candidate starts with.

<a id="freestylo.AlliterationAnnotation.AlliterationCandidate.score"></a>

#### score

```python
@property
def score()
```

This property returns the score of the alliteration candidate.

<a id="freestylo.AlliterationAnnotation.AlliterationCandidate.length"></a>

#### length

```python
@property
def length()
```

This property returns the length of the alliteration candidate.

<a id="freestylo.ChiasmusAnnotation"></a>

# freestylo.ChiasmusAnnotation

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation"></a>

## ChiasmusAnnotation Objects

```python
class ChiasmusAnnotation()
```

This class is used to find chiasmus candidates in a text.
It uses the TextObject class to store the text and its annotations.

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.__init__"></a>

#### \_\_init\_\_

```python
def __init__(text: TextObject, window_size=30)
```

Parameters
----------
text : TextObject
    The text to be analyzed.
window_size : int, optional
    The window size to search for chiasmus candidates

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.find_candidates"></a>

#### find\_candidates

```python
def find_candidates()
```

This method finds chiasmus candidates in the text.
It uses the window_size to search for candidates.

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.load_classification_model"></a>

#### load\_classification\_model

```python
def load_classification_model(model_path)
```

This method loads a classification model to score the chiasmus candidates.
Parameters
----------
model_path : str
    The path to the model file.

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.serialize"></a>

#### serialize

```python
def serialize() -> list
```

This method serializes the chiasmus candidates.

Returns
-------
list
    A list of serialized candidates.

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.has_candidates"></a>

#### has\_candidates

```python
def has_candidates()
```

This method checks if the text has chiasmus candidates.

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.score_candidates"></a>

#### score\_candidates

```python
def score_candidates()
```

This method scores the chiasmus candidates.

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.get_features"></a>

#### get\_features

```python
def get_features(candidate)
```

This method extracts features for a chiasmus candidate.

Parameters
----------
candidate : ChiasmusCandidate
    The candidate to extract features from.

Returns
-------
np.array
    An array of features.

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.get_dubremetz_features"></a>

#### get\_dubremetz\_features

```python
def get_dubremetz_features(candidate)
```

This method extracts Dubremetz features for a chiasmus candidate.

Returns
-------
np.array
    An array of Dubremetz features

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.get_lexical_features"></a>

#### get\_lexical\_features

```python
def get_lexical_features(candidate)
```

This method extracts lexical features for a chiasmus candidate.

Returns
-------
np.array
    An array of lexical features

<a id="freestylo.ChiasmusAnnotation.ChiasmusAnnotation.get_semantic_features"></a>

#### get\_semantic\_features

```python
def get_semantic_features(candidate)
```

This method extracts semantic features for a chiasmus candidate.

Returns
-------
np.array
    An array of semantic features

<a id="freestylo.ChiasmusAnnotation.cosine_similarity"></a>

#### cosine\_similarity

```python
def cosine_similarity(vec1, vec2)
```

This method calculates the cosine similarity between two vectors.

Parameters
----------
vec1 : np.array
    The first vector.
vec2 : np.array
    The second vector.

<a id="freestylo.ChiasmusAnnotation.ChiasmusCandidate"></a>

## ChiasmusCandidate Objects

```python
class ChiasmusCandidate()
```

This class represents a chiasmus candidate.

<a id="freestylo.ChiasmusAnnotation.ChiasmusCandidate.__init__"></a>

#### \_\_init\_\_

```python
def __init__(A, B, B_, A_)
```

Parameters
----------
A : int
    Index of the first supporting word
B : int
    Index of the second supporting word
B_ : int
    Index of the third supporting word, paired with B
A_ : int
    Index of the fourth supporting word, paired with A

<a id="freestylo.ChiasmusAnnotation.ChiasmusCandidate.__str__"></a>

#### \_\_str\_\_

```python
def __str__()
```

This method returns a string representation of the chiasmus candidate.

<a id="freestylo.__main__"></a>

# freestylo.\_\_main\_\_

<a id="freestylo.TextPreprocessor"></a>

# freestylo.TextPreprocessor

<a id="freestylo.TextPreprocessor.TextPreprocessor"></a>

## TextPreprocessor Objects

```python
class TextPreprocessor()
```

This class is used to preprocess text.
It uses the TextObject class to store the text and its annotations.

<a id="freestylo.TextPreprocessor.TextPreprocessor.__init__"></a>

#### \_\_init\_\_

```python
def __init__(language='en', max_length=None)
```

Constructor for the TextPreprocessor class.

Parameters
----------
language : str, optional
    The language of the text.

<a id="freestylo.TextPreprocessor.TextPreprocessor.load_spacy_nlp"></a>

#### load\_spacy\_nlp

```python
def load_spacy_nlp(model_name)
```

This method loads a spaCy model.

Parameters
----------
model_name : str
    The name of the spaCy model.

Returns
-------
spacy.lang
    The spaCy model.

<a id="freestylo.TextPreprocessor.TextPreprocessor.process_text"></a>

#### process\_text

```python
def process_text(text: TextObject)
```

This method processes a text.

<a id="freestylo.freestylo_main"></a>

# freestylo.freestylo\_main

<a id="freestylo.freestylo_main.main"></a>

#### main

```python
def main()
```

This is the main function of the freestylo tool.
When you run the tool from the command line, this function is called.
It reads the input text, preprocesses it, and adds the specified annotations.
The results are then serialized to a file.

<a id="freestylo.freestylo_main.report"></a>

#### report

```python
def report(args: argparse.Namespace)
```

This function is used to report the results of the analysis.
It takes the data file and the device to report as arguments.

<a id="freestylo.freestylo_main.build_chiasmus_sentence"></a>

#### build\_chiasmus\_sentence

```python
def build_chiasmus_sentence(tokens, ids)
```

This function builds a chiasmus sentence from the tokens and ids.
It takes the tokens and ids as arguments and returns the sentence as a list of strings.

<a id="freestylo.freestylo_main.report_chiasmus"></a>

#### report\_chiasmus

```python
def report_chiasmus(args: argparse.Namespace)
```

This function reports the results of the chiasmus analysis.
It takes the data file as an argument and prints the top chiasmus candidates.

<a id="freestylo.freestylo_main.annotate"></a>

#### annotate

```python
def annotate(args: argparse.Namespace)
```

This function is used to annotate the input text with the specified annotations.
It takes the input file, output file, and configuration file as arguments.
It loads the text, preprocesses it, and adds the specified annotations.
The results are then serialized to the output file.

<a id="freestylo.freestylo_main.add_chiasmus_annotation"></a>

#### add\_chiasmus\_annotation

```python
def add_chiasmus_annotation(text, config)
```

This function adds chiasmus annotations to the text.

<a id="freestylo.freestylo_main.add_metaphor_annotation"></a>

#### add\_metaphor\_annotation

```python
def add_metaphor_annotation(text, config)
```

This function adds metaphor annotations to the text.

<a id="freestylo.freestylo_main.add_epiphora_annotation"></a>

#### add\_epiphora\_annotation

```python
def add_epiphora_annotation(text, config)
```

This function adds epiphora annotations to the text.

<a id="freestylo.freestylo_main.add_polysyndeton_annotation"></a>

#### add\_polysyndeton\_annotation

```python
def add_polysyndeton_annotation(text, config)
```

This function adds polysyndeton annotations to the text.

<a id="freestylo.freestylo_main.add_alliteration_annotation"></a>

#### add\_alliteration\_annotation

```python
def add_alliteration_annotation(text, config)
```

This function adds alliteration annotations to the text.

<a id="freestylo.freestylo_main.get_longest_string"></a>

#### get\_longest\_string

```python
def get_longest_string(lines, index)
```

This function returns the longest string in a list of strings at a given index.

<a id="freestylo.freestylo_main.print_lines_aligned"></a>

#### print\_lines\_aligned

```python
def print_lines_aligned(lines)
```

This function prints a list of strings in a aligned format.

<a id="freestylo.SimilarityNN"></a>

# freestylo.SimilarityNN

<a id="freestylo.SimilarityNN.SimilarityNN"></a>

## SimilarityNN Objects

```python
class SimilarityNN(nn.Module)
```

This class defines a neural network for metaphor detection.

<a id="freestylo.SimilarityNN.SimilarityNN.__init__"></a>

#### \_\_init\_\_

```python
def __init__(input_dim, hidden_dim, num_hidden, output_dim, device)
```

Constructor for the SimilarityNN class.

Parameters
----------
input_dim : int
    The dimension of the input.
hidden_dim : int
    The dimension of the hidden layers.
num_hidden : int
    The number of hidden layers.
output_dim : int
    The dimension of the output.
device : str
    The device to run the model on.

<a id="freestylo.SimilarityNN.SimilarityNN.forward"></a>

#### forward

```python
def forward(data)
```

This method defines the forward pass of the neural network.

Parameters
----------
data : tensor
    The input data.

Returns
-------
tensor
    The output of the neural network.

<a id="freestylo.PolysyndetonAnnotation"></a>

# freestylo.PolysyndetonAnnotation

<a id="freestylo.PolysyndetonAnnotation.PolysyndetonAnnotation"></a>

## PolysyndetonAnnotation Objects

```python
class PolysyndetonAnnotation()
```

This class is used to find polysyndeton candidates in a text.
It uses the TextObject class to store the text and its annotations.

<a id="freestylo.PolysyndetonAnnotation.PolysyndetonAnnotation.__init__"></a>

#### \_\_init\_\_

```python
def __init__(text: TextObject,
             min_length=2,
             conj=["and", "or", "but", "nor"],
             sentence_end_tokens=[".", "?", "!", ":", ";", "..."],
             punct_pos="PUNCT")
```

Constructor for the PolysyndetonAnnotation class.

Parameters
----------
text : TextObject
    The text to be analyzed.
min_length : int, optional
    The minimum length of the polysyndeton candidates.
conj : list, optional
    A list of conjunctions that should be considered when looking for polysyndeton.
sentence_end_tokens : list, optional
    A list of tokens that indicate the end of a sentence.
punct_pos : str, optional
    The part of speech tag for punctuation.

<a id="freestylo.PolysyndetonAnnotation.PolysyndetonAnnotation.split_in_phrases"></a>

#### split\_in\_phrases

```python
def split_in_phrases()
```

This method splits the text into phrases.

Returns
-------
list
    A list of lists, each containing the start and end index of a phrase.

<a id="freestylo.PolysyndetonAnnotation.PolysyndetonAnnotation.check_add_candidate"></a>

#### check\_add\_candidate

```python
def check_add_candidate(candidates, candidate)
```

This method checks if the candidate is long enough to be a polysyndeton candidate.

Parameters
----------
candidates : list
    A list of polysyndeton candidates.

<a id="freestylo.PolysyndetonAnnotation.PolysyndetonAnnotation.find_candidates"></a>

#### find\_candidates

```python
def find_candidates()
```

This method finds polysyndeton candidates in the text.

<a id="freestylo.PolysyndetonAnnotation.PolysyndetonAnnotation.serialize"></a>

#### serialize

```python
def serialize() -> list
```

This method serializes the polysyndeton candidates.

Returns
-------
list
    A list of dictionaries, each containing the ids, word, and score of a polysyndeton candidate.

<a id="freestylo.PolysyndetonAnnotation.PolysyndetonCandidate"></a>

## PolysyndetonCandidate Objects

```python
class PolysyndetonCandidate()
```

This class represents a polysyndeton candidate.

<a id="freestylo.PolysyndetonAnnotation.PolysyndetonCandidate.__init__"></a>

#### \_\_init\_\_

```python
def __init__(ids, word)
```

Constructor for the PolysyndetonCandidate class.

Parameters
----------
ids : list
    A list of token ids that form the candidate.
word : str
    The word that the candidate ends with.

<a id="freestylo.PolysyndetonAnnotation.PolysyndetonCandidate.score"></a>

#### score

```python
@property
def score()
```

This property returns the score of the polysyndeton candidate.

<a id="freestylo.Configs"></a>

# freestylo.Configs

<a id="freestylo.Configs.get_model_path"></a>

#### get\_model\_path

```python
def get_model_path(model_to_load: str) -> str
```

This function checks if the model is already downloaded.
If not, it downloads the model from the given URL and extracts it.

<a id="freestylo.MetaphorAnnotation"></a>

# freestylo.MetaphorAnnotation

<a id="freestylo.MetaphorAnnotation.MetaphorAnnotation"></a>

## MetaphorAnnotation Objects

```python
class MetaphorAnnotation()
```

This class is used to find metaphor candidates in a text.
It uses the TextObject class to store the text and its annotations.

<a id="freestylo.MetaphorAnnotation.MetaphorAnnotation.__init__"></a>

#### \_\_init\_\_

```python
def __init__(text)
```

Constructor for the MetaphorAnnotation class.

Parameters
----------
text : TextObject
    The text to be analyzed.

<a id="freestylo.MetaphorAnnotation.MetaphorAnnotation.find_candidates"></a>

#### find\_candidates

```python
def find_candidates()
```

This method finds metaphor candidates in the text.

<a id="freestylo.MetaphorAnnotation.MetaphorAnnotation.serialize"></a>

#### serialize

```python
def serialize() -> list
```

This method serializes the metaphor candidates.

Returns
-------
list
    A list of dictionaries, each containing the ids of the adjective and noun, the adjective, the noun, and the score.

<a id="freestylo.MetaphorAnnotation.MetaphorAnnotation.load_model"></a>

#### load\_model

```python
def load_model(model_path)
```

This method loads a model for metaphor detection.

Parameters
----------
model_path : str
    The path to the model.

<a id="freestylo.MetaphorAnnotation.MetaphorAnnotation.get_vectors"></a>

#### get\_vectors

```python
def get_vectors()
```

This method returns the vectors of the adjective and noun candidates.

Returns
-------
np.array
    An array of adjective vectors.
np.array
    An array of noun vectors.

<a id="freestylo.MetaphorAnnotation.MetaphorAnnotation.score_candidates"></a>

#### score\_candidates

```python
def score_candidates()
```

This method scores the metaphor candidates.

<a id="freestylo.MetaphorAnnotation.cosine_distance"></a>

#### cosine\_distance

```python
def cosine_distance(a, b)
```

This function calculates the cosine distance between two vectors.

Parameters
----------
a : torch.Tensor
    The first vector.
b : torch.Tensor
    The second vector.

Returns
-------
float
    The cosine distance between the two vectors.

<a id="freestylo.MetaphorAnnotation.MetaphorCandidate"></a>

## MetaphorCandidate Objects

```python
class MetaphorCandidate()
```

This class represents a metaphor candidate.

<a id="freestylo.MetaphorAnnotation.MetaphorCandidate.__init__"></a>

#### \_\_init\_\_

```python
def __init__(adj_id, noun_id)
```

Constructor for the MetaphorCandidate class.

Parameters
----------
adj_id : int
    The id of the adjective.
noun_id : int
    The id of the noun.

