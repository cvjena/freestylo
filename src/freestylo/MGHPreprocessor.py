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

import cltk
import numpy as np
import fasttext
from freestylo.Configs import get_model_path

from cltk.corpus.middle_high_german.alphabet import normalize_middle_high_german
from cltk.tag.pos import POSTag
from cltk.lemmatize.middle_high_german.backoff import BackoffMHGLemmatizer



class MGHPreprocessor:
    """
    This class preprocesses Middle High German text.
    """
    def __init__(self):
        """
        Constructor for the MGHPreprocessor class.
        """
        self.text = ""
        self.model = fasttext.load_model(get_model_path("fasttext_mgh.bin"))
        pass

    # make class callable with ()
    def __call__(self, text):
        """
        This method preprocesses Middle High German text.
        
        Parameters
        ----------
        text : str
            The text to be preprocessed.

        Returns
        -------
        list
            A list of MGH tokens.
        """
        self.text = normalize_middle_high_german(text)

        tokens = []

        idx = 0
        pos_tagger = POSTag('middle_high_german')
        lemmatizer = BackoffMHGLemmatizer()
        # custom tokenizer, because I need the character index of the word
        while True:
            word, next_idx = self.get_next_word(self.text, idx)

            pos = pos_tagger.tag_tnt(word)[0][1]

            lemma = min(lemmatizer.lemmatize([word])[0][1], key=len)

            dep = ""

            vector = self.model.get_word_vector(word)


            tokens.append(MGHToken(word, pos, lemma, dep, vector, idx))

            if next_idx is None:
                break
            idx = next_idx
        return tokens



    def get_next_word(self, text, idx):
        """
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
        """
        cursor = idx
        is_end = False 
        # find end of current word
        while cursor < len(text):
            try:
                if text[cursor] in [" ", "\n", "\t"]:
                    break
            except: # end of text
                is_end = True
                break
            cursor += 1

        end_word = cursor

        #find start of next word
        while cursor < len(text):
            try:
                if text[cursor] not in [" ", "\n", "\t"]:
                    break
            except:
                is_end = True
                break
            cursor += 1

        next_word = cursor

        if cursor == len(text):
            next_word = None

        word = text[idx:end_word]

        return word, next_word

class MGHToken:
    """
    This class represents a Middle High German token.
    """
    def __init__(self, text, pos, lemma, dep, vector, idx):
        """
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
        """
        self.text = text
        self.pos = pos
        self.lemma = lemma
        self.dep = dep
        self.vector = vector
        self.idx = idx

