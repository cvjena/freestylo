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

import numpy as np
import freestylo.TextObject as to
import freestylo.TextPreprocessor as tp
import freestylo.AlliterationAnnotation as aa


def test_alliteration_annotation():
    """
    Test the AlliterationAnnotation class.
    """

    text = to.TextObject(
            text = "Toller Text, tierisch triftige Thesen! Aber manchmal auch keine Alliteration. So muss manchem, auch manchmal, manches durchaus mächtig missfallen.",
            language="de")
    preprocessor = tp.TextPreprocessor(language="de")
    preprocessor.process_text(text)

    alliteration = aa.AlliterationAnnotation(
            text = text,
            max_skip = 2,
            min_length = 3)

    alliteration.find_candidates()


    assert(len(alliteration.candidates) == 2)
    assert(text.tokens[alliteration.candidates[0].ids[0]] == "Toller")
    assert(text.tokens[alliteration.candidates[1].ids[0]] == "muss")
    assert(len(alliteration.candidates[0].ids) == 5)
    assert(len(alliteration.candidates[1].ids) == 6)





    for candidate in alliteration.candidates:
        print(" ".join(text.tokens[candidate.ids[0]:candidate.ids[-1]+1]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")




if __name__ == "__main__":
    test_alliteration_annotation()


