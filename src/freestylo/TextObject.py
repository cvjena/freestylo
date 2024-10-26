import pickle
import json

class TextObject:
    """
    This class is used to store a text and its annotations.
    """
    def __init__(self, textfile=None, text=None, language=''):
        """
        Constructor for the TextObject class.

        Parameters
        ----------
        textfile : str, optional
            The path to a text file.
        text : str, optional

        language : str, optional
            The language of the text.
        """
        self.textfile = textfile
        self.language = language
        self.tokens = []
        self.pos = []
        self.lemmas = []
        self.dep = []
        self.vectors = []
        self.annotations = []
        self.token_offsets = []
        self.text = text

        if textfile is not None:
            try:
                with open(textfile, 'r') as f:
                    self.text = f.read()
            except FileNotFoundError:
                print("File not found, no textfile loaded")
        elif text is not None:
            self.text = text

    def save_as(self, filename):
        """
        This method saves the TextObject as a pickle file.

        Parameters
        ----------
        filename : str
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def serialize(self, filename):
        """
        This method serializes the TextObject as a JSON file.

        Parameters
        ----------
        filename : str
        """
        with open(filename, 'w') as f:
            annotations = {}
            for anno in self.annotations:
                annotations[anno.type] = anno.serialize()
            save_dict = {
                'text': self.text,
                'tokens': self.tokens,
                'pos': self.pos,
                'lemmas': self.lemmas,
                'dep': self.dep,
                'token_offsets': self.token_offsets,
                'annotations': annotations
            }
            with open(filename, 'w') as f:
                json.dump(save_dict, f, indent=4)


    def has_text(self):
        """
        This method checks if the TextObject has a text.
        """
        return len(self.text) > 0
    
    def has_tokens(self):
        """
        This method checks if the TextObject has tokens.
        """ 
        return len(self.tokens) > 0

    def has_pos(self):
        """
        This method checks if the TextObject has part-of-speech tags.
        """
        return len(self.pos) > 0

    def has_lemmas(self):
        """
        This method checks if the TextObject has lemmas.
        """
        return len(self.lemmas) > 0

    def has_dep(self):
        """
        This method checks if the TextObject has dependency relations.
        """
        return len(self.dep) > 0

    def has_vectors(self):
        """
        This method checks if the TextObject has vectors.
        """
        return len(self.vectors) > 0

    def has_annotations(self):
        """
        This method checks if the TextObject has annotations.
        """
        return len(self.annotations) > 0
