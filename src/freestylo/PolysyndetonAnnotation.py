
from freestylo.TextObject import TextObject


class PolysyndetonAnnotation:
    """
    This class is used to find polysyndeton candidates in a text.
    It uses the TextObject class to store the text and its annotations.
    """
    def __init__(self, text : TextObject, min_length=2, conj = ["and", "or", "but", "nor"], sentence_end_tokens=[".", "?", "!", ":", ";", "..."], punct_pos="PUNCT"):
        """
        Constructor for the PolysyndetonAnnotation class.

        Parameters
        ----------
        text : TextObject
            The text to be analyzed.
        min_length : int, optional
            The minimum length of the polysyndeton candidates.
        conj : list, optional
            A list of conjunctions that should be considered when looking for polysyndeton.
        sentence_end_tokens : list, optional
            A list of tokens that indicate the end of a sentence.
        punct_pos : str, optional
            The part of speech tag for punctuation.
        """

        self.text = text
        self.candidates = []
        self.min_length = min_length
        self.conj = conj
        self.sentence_end_tokens = sentence_end_tokens
        self.punct_pos = punct_pos

    def split_in_phrases(self):
        """
        This method splits the text into phrases.

        Returns
        -------
        list
            A list of lists, each containing the start and end index of a phrase.
        """
        
        phrases_in_sentences = []
        phrases = []
        current_sentence_start = 0
        current_phrase_start = 0
        for i, token in enumerate(self.text.tokens):
            if token in self.sentence_end_tokens:
                phrases.append([current_phrase_start, i])
                current_phrase_start = i+1
                current_sentence_start = i+1
                phrases_in_sentences.append(phrases)
                phrases = []
            elif token in self.conj and i-current_phrase_start > 1:
                phrases.append([current_phrase_start, i])
                current_phrase_start = i
        return phrases_in_sentences

    def check_add_candidate(self, candidates, candidate):
        """
        This method checks if the candidate is long enough to be a polysyndeton candidate.

        Parameters
        ----------
        candidates : list
            A list of polysyndeton candidates.
        """
        if len(candidate.ids) >= self.min_length:
            candidates.append(candidate)
        return candidates



    def find_candidates(self):
        """
        This method finds polysyndeton candidates in the text.
        """
        candidates = []
        sentences = self.split_in_phrases()
        for sentence in sentences:
            current_candidate = PolysyndetonCandidate([], "")
            current_word = ""
            for phrase in sentence:
                word = self.text.tokens[phrase[0]]
                if word != current_candidate.word:
                    candidates = self.check_add_candidate(candidates, current_candidate)
                    current_candidate = PolysyndetonCandidate([phrase], word)
                else:
                    current_candidate.ids.append(phrase)
            candidates = self.check_add_candidate(candidates, current_candidate)

        self.candidates = []
        for candidate in candidates:
            if candidate.word in self.conj:
                self.candidates.append(candidate)


    def serialize(self) -> list:
        """
        This method serializes the polysyndeton candidates.

        Returns
        -------
        list
            A list of dictionaries, each containing the ids, word, and score of a polysyndeton candidate.
        """
        candidates = []
        for c in self.candidates:
            candidates.append({
                "ids": c.ids,
                "score": c.score,
                "word": c.word})
        return candidates


class PolysyndetonCandidate():
    """
    This class represents a polysyndeton candidate.
    """
    def __init__(self, ids, word):
        """
        Constructor for the PolysyndetonCandidate class.

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
        This property returns the score of the polysyndeton candidate.
        """
        return len(self.ids)
