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
from freestylo.MGHPreprocessor import MGHPreprocessor

class TextPreprocessor:
    """
    This class is used to preprocess text.
    It uses the TextObject class to store the text and its annotations.
    """
    def __init__(self, language='en', max_length=None):
        """
        Constructor for the TextPreprocessor class.

        Parameters
        ----------
        language : str, optional
            The language of the text.
        """

        if language == 'en':
            self.nlp = self.load_spacy_nlp('en_core_web_lg')
        elif language == 'de':
            self.nlp = self.load_spacy_nlp('de_core_news_lg')
        elif language == 'mgh':
            from MGHPreprocessor import MGHPreprocessor
            self.nlp = MGHPreprocessor()

        if max_length is not None:
            try:
                self.nlp.max_length = max_length
            except:
                print("Setting nlp max length not supported for middle high german, continue...")



    def load_spacy_nlp(self, model_name):
        """
        This method loads a spaCy model.

        Parameters
        ----------
        model_name : str
            The name of the spaCy model.

        Returns
        -------
        spacy.lang
            The spaCy model.
        """
        nlp = None
        while nlp is None:
            try:
                nlp = spacy.load(model_name)
            except:
                try:
                    spacy.cli.download(model_name)
                except:
                    print(f"ERROR: Could not download model {model_name}")
                    exit(1)
        return nlp


    def process_text(self, text : TextObject):
        """
        This method processes a text.
        """
        processed = self.nlp(text.text)
        try:
            text.tokens = [token.text for token in processed]
        except:
            print("No tokens available")

        try:    
            text.pos = [token.pos_ for token in processed]
        except:
            print("No POS available")

        try:
            text.lemmas = [token.lemma_ for token in processed]
        except:
            print("No lemmas available")

        try:
            text.dep = [token.dep_ for token in processed]
        except:
            print("No dependencies available")

        try:
            text.vectors = [token.vector for token in processed]
        except:
            print("No vectors available")

        try:
            text.token_offsets = [(token.idx, token.idx + len(token.text)) for token in processed]
        except:
            print("No token offsets available")


