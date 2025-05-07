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

from freestylo.TextObject import TextObject
from freestylo.TextPreprocessor import TextPreprocessor
from freestylo.MGHPreprocessor import MGHPreprocessor

import os
import json

def test_processing():
    """
    Test the TextObject and TextPreprocessor classes.
    """
    text = TextObject(text="This is a test sentence. This is another test sentence.", language='en')
    preprocessor = TextPreprocessor()
    preprocessor.process_text(text)
    assert text.has_tokens() == True
    assert len(text.tokens) == 12
    assert len(text.lemmas) == 12
    assert len(text.vectors) == 12
    print(text.tokens)


    text = "Das ist ein Test Satz. Das ist noch ein Test Satz."
    text = TextObject(text=text, language='de')
    preprocessor = TextPreprocessor()
    preprocessor.process_text(text)
    assert text.has_tokens() == True
    assert len(text.tokens) == 13
    assert len(text.lemmas) == 13
    assert len(text.vectors) == 13
    print(text.tokens)

    text = "Dô erbiten si der nahte und fuoren über Rîn"
    text = TextObject(text=text, language='mgh')
    preprocessor = TextPreprocessor()
    preprocessor.process_text(text)
    assert(len(text.tokens) == 9)
    assert(len(text.lemmas) == 9)
    assert(len(text.vectors) == 9)
    assert(text.has_tokens())
    print(text.tokens)



if __name__ == "__main__":
    test_processing()
