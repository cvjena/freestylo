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

"""
This class is used to find alliterations candidates in a text.
It uses the TextObject class to store the text and its annotations.
"""

class AlliterationAnnotation:
    """ This class is used to find alliterations candidates in a text.
    It uses the TextObject class to store the text and its annotations.
    """

    def __init__(self, text : TextObject, max_skip = 2, min_length=3, skip_tokens=[".", ",", ":", ";", "!", "?", "…", "(", ")", "[", "]", "{", "}", "„", "“", "‚", "‘:", "‘", "’"], ignore_tokens=None ):
        """
        Parameters
        ----------
        text : TextObject
            The text to be analyzed.
        max_skip : int, optional
        min_length : int, optional
        skip_tokens : list, optional
            A list of tokens that should be skipped when looking for alliterations.
        """

        self.text = text
        self.type = "alliteration"
        text.annotations.append(self)
        self.candidates = []
        self.max_skip = max_skip
        self.min_length = min_length
        self.skip_tokens = skip_tokens
        if ignore_tokens is not None:
            self.ignore_tokens = ignore_tokens
        else:
            self.ignore_tokens = []



    def find_candidates(self):
        """
        This method finds alliteration candidates in the text.
        """
        tokens = self.text.tokens

        open_candidates = {}
        i = 0

        for i in tqdm(range(len(tokens))):
            token = tokens[i]
            token_char = token[0].lower()
            # check if there is an  alliteration candidate with the current character
            if not token_char.isalpha():
                continue
            # if not, create a new one
            if token_char not in open_candidates and token_char not in self.skip_tokens and token_char not in self.ignore_tokens:
                open_candidates[token_char] = [AlliterationCandidate([i], token_char), 0]
                continue
            # if yes, add the current token to the candidate

            try:
                candidate = open_candidates[token_char][0]
            except KeyError:
                open_candidates[token_char] = [AlliterationCandidate([i], token_char), 0]
                candidate = open_candidates[token_char][0]

            if token not in self.skip_tokens and token not in self.ignore_tokens:
                candidate.ids.append(i)

            # close candidates
            keys_to_delete = []
            for key in open_candidates:
                candidate_pair = open_candidates[key]
                candidate = candidate_pair[0]
                if token_char in self.skip_tokens:
                    candidate_pair[1] += 1
                if i - candidate.ids[-1] >= self.max_skip+1+candidate_pair[1]:
                    if len(candidate.ids) > self.min_length:
                        self.candidates.append(candidate)
                    keys_to_delete.append(key)
            for key_del in keys_to_delete:
                    del open_candidates[key_del]
        # get the remaining ones
        for key in open_candidates:
            candidate = open_candidates[key][0]
            if len(candidate.ids) > self.min_length:
                self.candidates.append(candidate)



    def serialize(self) -> list:
        """
        This method serializes the alliteration candidates into a list of dictionaries.

        Returns
        -------
        list
            A list of dictionaries containing the ids, length and character of the alliteration candidates.
        """
        candidates = []
        for c in self.candidates:
            candidates.append({
                "ids": c.ids,
                "score": c.score,
                "char": c.char})
        return candidates


class AlliterationCandidate():
    """
    This class represents an alliteration candidate.
    """
    def __init__(self, ids, char):
        """
        Parameters
        ----------
        ids : list
            A list of token ids that form the alliteration candidate.
        char : str
            The character that the candidate starts with.
        """
        self.ids = ids
        self.char = char

    @property
    def score(self):
        """
        This property returns the score of the alliteration candidate.
        """
        return len(self.ids)

    @property
    def length(self):
        """
        This property returns the length of the alliteration candidate.
        """
        return len(self.ids)
