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
from freestylo.Configs import get_model_path
from tqdm import tqdm
import numpy as np

class ChiasmusAnnotation:
    """
    This class is used to find chiasmus candidates in a text.
    It uses the TextObject class to store the text and its annotations.
    """
    def __init__(self, text : TextObject, window_size=30):
        """
        Parameters
        ----------
        text : TextObject
            The text to be analyzed.
        window_size : int, optional
            The window size to search for chiasmus candidates
        """
        self.text = text
        text.annotations.append(self)
        self.window_size = window_size
        self.candidates = []
        self.denylist = []
        self.allowlist = []
        self.neglist = []
        self.poslist = []
        self.conjlist = []
        self.type = "chiasmus"
        self.model = None


    def find_candidates(self):
        """
        This method finds chiasmus candidates in the text.
        It uses the window_size to search for candidates.
        """
        pos = self.text.pos

        outer_matches = []
        for i in tqdm(range(len(pos))):
            outer_matches += self._find_matches(i, i + self.window_size)

        for match in tqdm(outer_matches):
            A, A_ = match
            for i in tqdm(range(match[0]+1, match[1])):
                inner_matches = self._find_matches(i, match[1])
                for B, B_ in inner_matches:
                    self.candidates.append(ChiasmusCandidate(A, B, B_, A_))

    def load_classification_model(self, model_path):
        """
        This method loads a classification model to score the chiasmus candidates.
        Parameters
        ----------
        model_path : str
            The path to the model file.
        """
        import pickle
        with open(get_model_path(model_path), "rb") as f:
            self.model = pickle.load(f)

    def serialize(self) -> list:
        """
        This method serializes the chiasmus candidates.

        Returns
        -------
        list
            A list of serialized candidates.
        """
        candidates = []
        for c in self.candidates:
            candidates.append({
        "ids": c.ids,
        "A": c.A,
        "B": c.B,
        "B_": c.B_,
        "A_": c.A_,
        "score": c.score})
        return candidates



    def _find_matches(self, start : int, end : int) -> list:
        """
        This method finds matches in the pos list of the text.
        It uses the start and end index to search for matches.

        Parameters
        ----------
        start : int
            The start index of the search.
        end : int
            The end index of the search.
        """
        pos = self.text.pos

        #if end > len(pos):
        #    end = len(pos)

        #if end < start+3:
        #    return []

        if not self._check_pos(pos[start]):
            return []
        matches = []
        for i in range(start+1, end):
            try:
                if pos[start] == pos[i]:
                    matches.append((start, i))
            except IndexError:
                pass
        return matches

    def _check_pos(self, pos):
        """
        This method checks if a pos is in the allowlist or not in the denylist.

        Parameters
        ----------
        pos : str
            The pos to check.
        """
        if len(self.allowlist) > 0 and pos not in self.allowlist:
            return False
        if len(self.denylist) > 0 and pos in self.denylist:
            return False
        return True

    def has_candidates(self):
        """
        This method checks if the text has chiasmus candidates.
        """
        return len(self.candidates) > 0

    def score_candidates(self):
        """
        This method scores the chiasmus candidates.
        """
        features = []
        for candidate in tqdm(self.candidates):
            features.append(self.get_features(candidate))
        if self.model is None:
            print("Load Chiasmus Model before scoring the candidates")
            return False
        features = np.stack(features)
        print("   scoring....")
        scores = self.model.decision_function(features)
        print("   Done scoring")
        for score, candidate in zip(scores, self.candidates):
            candidate.score = score
        return True

    def get_features(self, candidate):
        """
        This method extracts features for a chiasmus candidate.

        Parameters
        ----------
        candidate : ChiasmusCandidate
            The candidate to extract features from.

        Returns
        -------
        np.array
            An array of features.
        """

        dubremetz_features = self.get_dubremetz_features(candidate)
        lexical_features = self.get_lexical_features(candidate)
        semantic_features = self.get_semantic_features(candidate)
        return np.concatenate((dubremetz_features, lexical_features, semantic_features))

    def get_dubremetz_features(self, candidate):
        """
        This method extracts Dubremetz features for a chiasmus candidate.

        Returns
        -------
        np.array
            An array of Dubremetz features
        """
        tokens = self.text.tokens
        lemmas = self.text.lemmas
        pos = self.text.pos
        dep = self.text.dep
        vectors = self.text.vectors

        context_start = candidate.A - 5
        context_end = candidate.A_ + 5

        tokens_main = [tokens[i] for i in range(candidate.A, candidate.A_+1)]
        lemmas_main = [lemmas[i] for i in range(candidate.A, candidate.A_+1)]
        pos_main = [pos[i] for i in range(candidate.A, candidate.A_+1)]
        dep_main = [dep[i] for i in range(candidate.A, candidate.A_+1)]
        vectors_main = [vectors[i] for i in range(candidate.A, candidate.A_+1)]

        neglist = self.neglist
        poslist = self.poslist
        conjlist = self.conjlist

        hardp_list = ['.', '(', ')', "[", "]"]
        softp_list = [',', ';']

        features = []

         # Basic

        num_punct = 0
        for h in hardp_list:
            if h in tokens[ candidate.ids[0]+1 : candidate.ids[1] ]: num_punct+=1
            if h in tokens[ candidate.ids[2]+1 : candidate.ids[3] ]: num_punct+=1
        features.append(num_punct)

        num_punct = 0
        for h in hardp_list:
            if h in tokens[ candidate.ids[0]+1 : candidate.ids[1] ]: num_punct+=1
            if h in tokens[ candidate.ids[2]+1 : candidate.ids[3] ]: num_punct+=1
        features.append(num_punct)

        num_punct = 0
        for h in hardp_list:
            if h in tokens[ candidate.ids[1]+1 : candidate.ids[2] ]: num_punct+=1
        features.append(num_punct)

        rep_a1 = -1
        if lemmas[candidate.ids[0]] == lemmas[candidate.ids[3]]:
            rep_a1 -= 1
        rep_a1 += lemmas.count(lemmas[candidate.ids[0]])
        features.append(rep_a1)

        rep_b1 = -1
        if lemmas[candidate.ids[1]] == lemmas[candidate.ids[2]]:
            rep_b1 -= 1
        rep_b1 += lemmas.count(lemmas[candidate.ids[1]])
        features.append(rep_b1)

        rep_b2 = -1
        if lemmas[candidate.ids[1]] == lemmas[candidate.ids[2]]:
            rep_b2 -= 1
        rep_b2 += lemmas.count(lemmas[candidate.ids[2]])
        features.append(rep_b2)

        rep_a2 = -1
        if lemmas[candidate.ids[0]] == lemmas[candidate.ids[3]]:
            rep_a2 -= 1
        rep_a2 += lemmas.count(lemmas[candidate.ids[3]])
        features.append(rep_b2)

        # Size

        diff_size = abs((candidate.ids[1]-candidate.ids[0]) - (candidate.ids[3]-candidate.ids[2]))
        features.append(diff_size)

        toks_in_bc = candidate.ids[3]-candidate.ids[1]
        features.append(toks_in_bc)

        # Similarity

        exact_match = ([" ".join(tokens[candidate.ids[0]+1 : candidate.ids[1]])] == [" ".join(tokens[candidate.ids[2]+1 : candidate.ids[3]])])
        features.append(exact_match)

        same_tok = 0
        for l in lemmas[candidate.ids[0]+1 : candidate.ids[1]]:
            if l in lemmas[candidate.ids[2]+1 : candidate.ids[3]]: same_tok += 1
        features.append(same_tok)

        sim_score = same_tok / (candidate.ids[1]-candidate.ids[0])
        features.append(sim_score)

        num_bigrams = 0
        t1 = " ".join(tokens[candidate.ids[0]+1 : candidate.ids[1]])
        t2 = " ".join(tokens[candidate.ids[2]+1 : candidate.ids[3]])
        s1 = set()
        s2 = set()
        for t in range(len(t1)-1):
            bigram = t1[t:t+2]
            s1.add(bigram)
        for t in range(len(t2)-1):
            bigram = t2[t:t+2]
            s2.add(bigram)
        for b in s1:
            if b in s2: num_bigrams += 1
        bigrams_normed = (num_bigrams/max(len(s1)+1, len(s2)+1))
        features.append(bigrams_normed)

        num_trigrams = 0
        t1 = " ".join(tokens[candidate.ids[0]+1 : candidate.ids[1]])
        t2 = " ".join(tokens[candidate.ids[2]+1 : candidate.ids[3]])
        s1 = set()
        s2 = set()
        for t in range(len(t1)-2):
            trigram = t1[t:t+3]
            s1.add(trigram)
        for t in range(len(t2)-2):
            trigram = t2[t:t+3]
            s2.add(trigram)
        for t in s1:
            if t in s2: num_trigrams += 1
        trigrams_normed = (num_trigrams/max(len(s1)+1, len(s2)+1))
        features.append(trigrams_normed)

        same_cont = 0
        t1 = set(tokens[candidate.ids[0]+1:candidate.ids[1]])
        t2 = set(tokens[candidate.ids[2]+1:candidate.ids[3]])
        for t in t1:
            if t in t2: same_cont += 1
        features.append(same_cont)

        # Lexical clues

        conj = 0
        for c in conjlist:
            if c in tokens[candidate.ids[1]+1:candidate.ids[2]]+lemmas[candidate.ids[1]+1:candidate.ids[2]]:
                conj = 1
        features.append(conj)


        neg = 0
        for n in neglist:
            if n in tokens[candidate.ids[1]+1:candidate.ids[2]]+lemmas[candidate.ids[1]+1:candidate.ids[2]]:
                neg = 1
        features.append(neg)


        # Dependency score

        if dep[candidate.ids[1]] == dep[candidate.ids[3]]:
            features.append(1)
        else:
            features.append(0)

        if dep[candidate.ids[0]] == dep[candidate.ids[2]]:
            features.append(1)
        else:
            features.append(0)

        if dep[candidate.ids[1]] == dep[candidate.ids[2]]:
            features.append(1)
        else:
            features.append(0)

        if dep[candidate.ids[0]] == dep[candidate.ids[3]]:
            features.append(1)
        else:
            features.append(0)

        features = np.array(features)
        return features

    def get_lexical_features(self, candidate):
        """
        This method extracts lexical features for a chiasmus candidate.

        Returns
        -------
        np.array
            An array of lexical features
        """
        tokens = self.text.tokens
        lemmas = self.text.lemmas
        pos = self.text.pos
        dep = self.text.dep
        vectors = self.text.vectors

        context_start = candidate.A - 5
        context_end = candidate.A_ + 5

        lemmas_main = [lemmas[i] for i in candidate.ids]


        neglist = self.neglist
        poslist = self.poslist

        features = []


        for i in range(len(lemmas_main)):
            for j in range(i+1, len(lemmas_main)):
                if lemmas_main[i] == lemmas_main[j]:
                    features.append(1)
                else:
                    features.append(0)

        features = np.array(features)
        return features

    def get_semantic_features(self, candidate):
        """
        This method extracts semantic features for a chiasmus candidate.

        Returns
        -------
        np.array
            An array of semantic features
        """
        tokens = self.text.tokens
        lemmas = self.text.lemmas
        pos = self.text.pos
        dep = self.text.dep
        vectors = self.text.vectors

        context_start = candidate.A - 5
        context_end = candidate.A_ + 5

        vectors_main = [vectors[i] for i in candidate.ids]


        features = []
        for i in range(len(vectors_main)):
            for j in range(i+1, len(vectors_main)):
                features.append(cosine_similarity(vectors_main[i], vectors_main[j]))

        features = np.array(features)
        return features



def cosine_similarity(vec1, vec2):
    """
    This method calculates the cosine similarity between two vectors.

    Parameters
    ----------
    vec1 : np.array
        The first vector.
    vec2 : np.array
        The second vector.
    """
    result = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    if np.isnan(result):
        result = 0
    return result


class ChiasmusCandidate:
    """
    This class represents a chiasmus candidate.
    """
    def __init__(self, A, B, B_, A_):
        """
        Parameters
        ----------
        A : int
            Index of the first supporting word
        B : int
            Index of the second supporting word
        B_ : int
            Index of the third supporting word, paired with B
        A_ : int
            Index of the fourth supporting word, paired with A
        """

        self.ids = [A, B, B_, A_]
        self.A = A
        self.B = B
        self.B_ = B_
        self.A_ = A_
        self.score = None

    def __str__(self):
        """
        This method returns a string representation of the chiasmus candidate.
        """
        return f"{self.A} {self.B} {self.B_} {self.A_}"


