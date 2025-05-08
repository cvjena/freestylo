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

import spacy
from freestylo.TextObject import TextObject
import freestylo.ChiasmusAnnotation as ca
import numpy as np

def preprocess_data(text : str):
    nlp = None
    model_name = "es_core_news_sm"
    while nlp is None:
        try:
            nlp = spacy.load(model_name)
        except:
            try:
                spacy.cli.download(model_name)
            except:
                print(f"ERROR: Could not download model {model_name}")
                exit(1)

    doc = nlp(text)
    return doc


def test_external():
    """
    This test shows how to fill the TextObject with external data.
    You can use this when you e.g. want to use the TextObject with a custom preprocessor.
    """

    text = "La música está alta y enojados están los vecinos. Esta es otra frase interesante."
    doc = preprocess_data(text)

    text_object = TextObject(text=text, language='es')
    text_object.tokens = [token.text for token in doc]
    text_object.lemmas = [token.lemma_ for token in doc]
    text_object.pos = [token.pos_ for token in doc]
    text_object.vectors = [token.vector for token in doc]
    text_object.dep = [token.dep_ for token in doc]

    chiasmus = ca.ChiasmusAnnotation(
            text=text_object)
    chiasmus.allowlist = ["NOUN", "VERB", "ADJ", "ADV"]
    chiasmus.find_candidates()
    chiasmus.load_classification_model("chiasmus_de.pkl")
    chiasmus.score_candidates()

    scores = [c.score for c in chiasmus.candidates]
    indices = np.argsort(scores)[::-1]

    best_candidate = chiasmus.candidates[indices[0]]
    best_tokens = " ".join(text_object.tokens[best_candidate.A:best_candidate.A_+1])
    assert(best_tokens == "música está alta y enojados están los vecinos")
    assert(best_candidate.A == 1) # música
    assert(best_candidate.B == 3) # alta
    assert(best_candidate.B_ == 5) # enojados
    assert(best_candidate.A_ == 8) # vecinos


if __name__ == "__main__":
    test_external()
