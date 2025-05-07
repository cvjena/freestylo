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

import freestylo.TextObject as to
import freestylo.PolysyndetonAnnotation as pa
import freestylo.TextPreprocessor as tp
import numpy as np



def test_polysyndeton_annotation():
    """
    Test the PolysyndetonAnnotation class.
    """
    text = to.TextObject(
            text = "Yesterday I wrote, and read, and then I slept, and then I woke up, and then I wrote again. This is a sentence. This is another sentence, and a short one at that.",
            language="de")
    preprocessor = tp.TextPreprocessor(language="en")
    preprocessor.process_text(text)

    polysysndeton = pa.PolysyndetonAnnotation(
            text = text,
            min_length = 2,
            conj = ["and", "or", "but", "nor"])

    polysysndeton.find_candidates()


    candidate = polysysndeton.candidates[0]
    assert(len(polysysndeton.candidates) == 1)
    assert(len(candidate.ids) == 4)
    assert(candidate.word == "and")

    for candidate in polysysndeton.candidates:
        print(" ".join(text.tokens[candidate.ids[0][0]:candidate.ids[-1][-1]+1]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")


if __name__ == "__main__":
    test_polysyndeton_annotation()


