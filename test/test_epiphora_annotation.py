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
import freestylo.EpiphoraAnnotation as ea
import freestylo.TextPreprocessor as tp
import numpy as np



def test_epiphora_annotation():
    """
    Test the EpiphoraAnnotation class.
    """
    text = to.TextObject(
            text = "Yesterday I thought of the paper, then I wrote the paper, now I am publishing the paper. I also write another sentence, that consists of mulitple phrases, they all have different endings.",
            language="de")
    preprocessor = tp.TextPreprocessor(language="en")
    preprocessor.process_text(text)

    epiphora = ea.EpiphoraAnnotation(
            text = text,
            min_length = 2,
            conj = ["and", "or", "but", "nor"])

    epiphora.find_candidates()


    candidate = epiphora.candidates[0]

    assert(len(epiphora.candidates) == 1)
    assert(len(candidate.ids) == 3)

    for candidate in epiphora.candidates:
        print(" ".join(text.tokens[candidate.ids[0][0]:candidate.ids[-1][-1]+1]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")


if __name__ == "__main__":
    test_epiphora_annotation()


