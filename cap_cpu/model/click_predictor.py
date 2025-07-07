import torch
import numpy as np
from model.lstm_model import LSTMClassifier


class ClickPredictor:
    def __init__(self, model_path="assets/models/lstm_of_Z_v6.pt"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = LSTMClassifier(input_size=1, hidden_size=32)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

    def predict(self, sequence):
        sequence = np.array(sequence)
        if np.max(sequence) != 0:
            sequence = sequence / np.max(sequence)
        input_tensor = torch.tensor(sequence, dtype=torch.float32).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(input_tensor)
            pred = torch.argmax(output, dim=1).item()
        return pred