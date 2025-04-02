import numpy as np

class SimpleLSTM:
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.init_weights()

    def init_weights(self):
        self.Wf = np.random.randn(self.hidden_dim, self.input_dim + self.hidden_dim)
        self.Wi = np.random.randn(self.hidden_dim, self.input_dim + self.hidden_dim)
        self.Wc = np.random.randn(self.hidden_dim, self.input_dim + self.hidden_dim)
        self.Wo = np.random.randn(self.hidden_dim, self.input_dim + self.hidden_dim)
        self.Wy = np.random.randn(self.output_dim, self.hidden_dim)

    def forward(self, inputs):
        h, c = np.zeros((self.hidden_dim, 1)), np.zeros((self.hidden_dim, 1))
        outputs = []
        for x in inputs:
            x = x.reshape(-1, 1)
            concat = np.vstack((h, x))
            f = self.sigmoid(self.Wf @ concat)
            i = self.sigmoid(self.Wi @ concat)
            c_bar = np.tanh(self.Wc @ concat)
            c = f * c + i * c_bar
            o = self.sigmoid(self.Wo @ concat)
            h = o * np.tanh(c)
            y = self.Wy @ h
            outputs.append(y.flatten())
        return np.array(outputs)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
