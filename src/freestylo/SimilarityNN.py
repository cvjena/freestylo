import torch.nn as nn
class SimilarityNN(nn.Module):
    """
    This class defines a neural network for metaphor detection.
    """
    def __init__(self, input_dim, hidden_dim, num_hidden, output_dim, device):
        """
        Constructor for the SimilarityNN class.

        Parameters
        ----------
        input_dim : int
            The dimension of the input.
        hidden_dim : int
            The dimension of the hidden layers.
        num_hidden : int
            The number of hidden layers.
        output_dim : int
            The dimension of the output.
        device : str
            The device to run the model on.
        """
        super(SimilarityNN, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_hidden = num_hidden
        self.output_dim = output_dim

        self.input_layer = nn.Linear(input_dim, hidden_dim, device=device)
        self.hidden_layers = nn.ModuleList()
        for i in range(num_hidden):
            self.hidden_layers.append(nn.Linear(hidden_dim, hidden_dim, device=device))
        self.output_layer = nn.Linear(hidden_dim, self.output_dim, device=device)


    def forward(self, data):
        """
        This method defines the forward pass of the neural network.

        Parameters
        ----------
        data : tensor
            The input data.

        Returns
        -------
        tensor
            The output of the neural network.
        """
        intermediate = [nn.ReLU()(self.input_layer(data))]
        for i in range(self.num_hidden):
            intermediate.append(nn.ReLU()(self.hidden_layers[i](intermediate[i])))
        out = self.output_layer(intermediate[-1])
        return out

