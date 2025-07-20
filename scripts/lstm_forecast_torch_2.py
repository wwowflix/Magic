# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

def run_lstm_forecast(csv_file, keyword):
    print("? Running PyTorch LSTM forecast...")

    df = pd.read_csv(csv_file)
    df_filtered = df[df["keyword"] == keyword]
    print("DataFrame shape after keyword filter:", df_filtered.shape)
    print(df_filtered.head())

    if df_filtered.empty:
        print(f"No data for keyword: {keyword}")
        return

    # Preprocess
    data = df_filtered["value"].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # Prepare sequences
    seq_length = min(2, len(df_filtered["value"])-1)
    print("Using sequence length:", seq_length)
    print("Using sequence length:", seq_length)
    X = []
    y = []

    for i in range(len(data_scaled) - seq_length):
        X.append(data_scaled[i:i+seq_length])
        y.append(data_scaled[i+seq_length])

    X = np.array(X)
    y = np.array(y)

    X_tensor = torch.from_numpy(X).float()
    y_tensor = torch.from_numpy(y).float()

    # Define model
    model = LSTMModel(input_size=1, hidden_size=50, num_layers=2, output_size=1)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    # Train
    for epoch in range(30):
        model.train()
        output = model(X_tensor)
        loss = criterion(output, y_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if epoch % 5 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    # Predict
    model.eval()
    predictions = model(X_tensor).detach().numpy()
    predictions_rescaled = scaler.inverse_transform(predictions)

    # Plot
    plt.figure(figsize=(10,5))
    plt.plot(df_filtered["date"].values[seq_length:], predictions_rescaled, label="Forecast")
    plt.plot(df_filtered["date"].values, df_filtered["value"].values, label="Actual")
    plt.legend()
    plt.title(f"PyTorch LSTM Forecast for {keyword}")
    plt.show()

if __name__ == "__main__":
    run_lstm_forecast("outputs/google_trends.csv", "ai tools")



