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
import torch
import freestylo.SimilarityNN as SimilarityNN
from freestylo.TextObject import TextObject
from freestylo.Configs import get_model_path
from tqdm import tqdm



class MetaphorAnnotation:
    """
    This class is used to find metaphor candidates in a text.
    It uses the TextObject class to store the text and its annotations.
    """
    def __init__(self, text):
        """
        Constructor for the MetaphorAnnotation class.

        Parameters
        ----------
        text : TextObject
            The text to be analyzed.
        """
        self.text = text
        text.annotations.append(self)
        self.candidates = []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.type = "metaphor"
        self.model = None

    def find_candidates(self):
        """
        This method finds metaphor candidates in the text.
        """
        pos = self.text.pos
        for i in tqdm(range(len(pos)-1)):
            if pos[i] == "ADJ" and pos[i+1] == "NOUN":
                self.candidates.append(MetaphorCandidate(i, i+1))

    def serialize(self) -> list:
        """
        This method serializes the metaphor candidates.

        Returns
        -------
        list
            A list of dictionaries, each containing the ids of the adjective and noun, the adjective, the noun, and the score.
        """
        candidates = []
        for c in self.candidates:
            candidates.append({
                "ids": c.ids,
                "adjective": c.adj_id,
                "noun": c.noun_id,
                "score": c.score})
        return candidates


    def load_model(self, model_path):
        """
        This method loads a model for metaphor detection.

        Parameters
        ----------
        model_path : str
            The path to the model.
        """
        model_path = get_model_path(model_path)
        input_size = 300
        if self.text.language == "mgh":
            input_size = 100
        self.model = SimilarityNN.SimilarityNN(input_size, 128, 1, 128, self.device)
        self.model.load_state_dict(torch.load(model_path, weights_only=True, map_location=self.device))
        self.model = self.model.to(self.device)
        self.model.eval()

    def get_vectors(self):
        """
        This method returns the vectors of the adjective and noun candidates.

        Returns
        -------
        np.array
            An array of adjective vectors.
        np.array
            An array of noun vectors.
        """
        adj_vectors = []
        noun_vectors = []
        for candidate in self.candidates:
            adj_vectors.append(self.text.vectors[candidate.ids[0]])
            noun_vectors.append(self.text.vectors[candidate.ids[1]])

        adj_vectors = np.array(adj_vectors)
        noun_vectors = np.array(noun_vectors)
        return adj_vectors, noun_vectors

    def score_candidates(self):
        """
        This method scores the metaphor candidates.
        """
        adj_vectors, noun_vectors = self.get_vectors()
        adj_tensor = torch.tensor(adj_vectors, device=self.device).to(self.device)
        noun_tensor = torch.tensor(noun_vectors, device=self.device).to(self.device)
        assert(self.model is not None)
        adj_metaphor_tensor = self.model(adj_tensor)
        noun_metaphor_tensor = self.model(noun_tensor)
        #scores = 1-(torch.nn.CosineSimilarity()(adj_metaphor_tensor, noun_metaphor_tensor)+1)/2
        print("   scoring...")
        scores = cosine_distance(adj_metaphor_tensor, noun_metaphor_tensor)
        print("   done")
        for score, candidate in zip(scores, self.candidates):
            candidate.score = score.item()

def cosine_distance(a, b):
    """
    This function calculates the cosine distance between two vectors.

    Parameters
    ----------
    a : torch.Tensor
        The first vector.
    b : torch.Tensor
        The second vector.

    Returns
    -------
    float
        The cosine distance between the two vectors.
    """
    return 1 - torch.nn.functional.cosine_similarity(a, b)

class MetaphorCandidate():
    """
    This class represents a metaphor candidate.
    """
    def __init__(self, adj_id, noun_id):
        """
        Constructor for the MetaphorCandidate class.

        Parameters
        ----------
        adj_id : int
            The id of the adjective.
        noun_id : int
            The id of the noun.
        """
        self.ids = [adj_id, noun_id]
        self.noun_id = noun_id
        self.adj_id = adj_id
        self.score = None

