
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
from tqdm import tqdm


class EpiphoraAnnotation:
    """
    This class is used to find epiphora candidates in a text.
    It uses the TextObject class to store the text and its annotations.
    """
    def __init__(self, text : TextObject, min_length=2, conj = ["and", "or", "but", "nor"], punct_pos="PUNCT"):
        """
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
        """

        self.text = text
        self.type = "epiphora"
        text.annotations.append(self)
        self.candidates = []
        self.min_length = min_length
        self.conj = conj
        self.punct_pos = punct_pos

    def split_in_phrases(self):
        """
        This method splits the text into phrases.

        Returns
        -------
        list
            A list of lists, each containing the start and end index of a phrase.
        """
            
        phrases = []
        current_start = 0
        punct_tokens = [".", "!", "?", ":", ";", ","]
        for i, token in tqdm(enumerate(self.text.tokens)):
            if token in self.conj or self.text.pos[i] == self.punct_pos or self.text.pos[i] in ["CONJ", "CCONJ"] or self.text.tokens[i].lower() in punct_tokens:
                if i-current_start > 2:
                    phrases.append([current_start, i-1])
                    current_start = i
                elif token in [".", "!", "?"]:
                    phrases.append([current_start, i-1])
                    current_start = i
        phrases.append([current_start, len(self.text.tokens)-1])
        return phrases


    def find_candidates(self):
        """
        This method finds epiphora candidates in the text.
        """
        candidates = []
        current_candidate = EpiphoraCandidate([], "")
        phrases = self.split_in_phrases()
        #for p in phrases:
        #    print("###")
        #    print(" ".join(self.text.tokens[p[0]:p[1]+1]))
        for phrase in tqdm(phrases):
            word = self.text.tokens[phrase[1]]
            if word != current_candidate.word:
                if len(current_candidate.ids) >= self.min_length:
                    candidates.append(current_candidate)
                current_candidate = EpiphoraCandidate([phrase], word)
            else:
                current_candidate.ids.append(phrase)
        self.candidates = candidates

    def serialize(self) -> list:
        """
        This method serializes the epiphora candidates.

        Returns
        -------
        list
            A list of dictionaries, each containing the ids, length, and word of an epiphora candidate.
        """
        candidates = []
        for c in self.candidates:
            candidates.append({
                "ids": c.ids,
                "score": c.score,
                "word": c.word})
        return candidates


class EpiphoraCandidate():
    """
    This class represents an epiphora candidate.
    """
    def __init__(self, ids, word):
        """
        Constructor for the EpiphoraCandidate class.

        Parameters
        ----------
        ids : list
            A list of token ids that form the candidate.
        word : str
            The word that the candidate ends with.
        """
        self.ids = ids
        self.word = word

    @property
    def score(self):
        """
        This property returns the score of the candidate.
        """
        return len(self.ids)
