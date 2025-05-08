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

import freestylo.ChiasmusAnnotation as ca
import freestylo.TextObject as to
import freestylo.TextPreprocessor as tp
import numpy as np


def test_chiasmus_annotation():
    """
    Test the ChiasmusAnnotation class.
    """

    text = to.TextObject(
            text = """Wörter gibt es häufig, doch selten sind die Beispiele.
Das ist noch ein Satz mit einem schönen Adjektiv.""",
            language="de")
    preprocessor = tp.TextPreprocessor(language="de")
    preprocessor.process_text(text)


    chiasmus = ca.ChiasmusAnnotation(
            text=text)
    chiasmus.allowlist = ["NOUN", "VERB", "ADJ", "ADV"]
    chiasmus.find_candidates()
    chiasmus.load_classification_model("chiasmus_de.pkl")
    chiasmus.score_candidates()

    scores = [c.score for c in chiasmus.candidates]
    indices = np.argsort(scores)[::-1]

    best_candidate = chiasmus.candidates[indices[0]]
    best_tokens = " ".join(text.tokens[best_candidate.A:best_candidate.A_+1])
    assert(best_tokens == "Wörter gibt es häufig , doch selten sind die Beispiele")
    assert(best_candidate.A == 0) # Wörter
    assert(best_candidate.B == 3) # häufig
    assert(best_candidate.B_ == 6) # selten
    assert(best_candidate.A_ == 9) # Beispiele


    for candidate in chiasmus.candidates:
        print(" ".join(text.tokens[candidate.A:candidate.A_+1]))
        print()
        print(" ".join(text.pos[candidate.A:candidate.A_+1]))
        print()
        print("tokens:", " ".join([text.tokens[i] for i in candidate.ids]))
        print("pos:", " ".join([text.pos[i] for i in candidate.ids]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")




if __name__ == "__main__":
    test_chiasmus_annotation()


