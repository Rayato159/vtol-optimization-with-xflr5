import numpy as np

class NN:
    def __init__(self, input_size, hidden_layer, output_size):
        self.input_size = input_size
        self.hidden_layer = hidden_layer
        self.output_size = output_size

        self.weight = np.random.rand()

    def forward_feed(self):
        for index, _ in enumerate(self.hidden_layer):
            pass

    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))

model = NN(2, 3, 1)