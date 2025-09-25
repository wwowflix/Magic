# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler


def run_lstm_forecast(csv_file, keyword):
    print("-> Running LSTM forecast...")

    # Load your CSV
    df = pd.read_csv(csv_file)
    df_filtered = df[df["keyword"] == keyword]

    if df_filtered.empty:
        print(f"No data found for keyword: {keyword}")
        return

    data = df_filtered["value"].values.reshape(-1, 1)

    # Scale data
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # Prepare sequences
    X = []
    y = []
    window_size = 10
    for i in range(len(data_scaled) - window_size):
        X.append(data_scaled[i : i + window_size, 0])
        y.append(data_scaled[i + window_size, 0])

    X = np.array(X)
    y = np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Build model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mean_squared_error")

    model.fit(X, y, epochs=10, batch_size=16, verbose=1)

    predictions = model.predict(X)
    predictions_rescaled = scaler.inverse_transform(predictions)

    # Plot results
    plt.plot(
        df_filtered["date"].iloc[window_size:].values,
        predictions_rescaled,
        label="Forecast",
    )
    plt.plot(df_filtered["date"], df_filtered["value"], label="Actual")
    plt.legend()
    plt.title(f"LSTM Forecast for {keyword}")
    plt.show()


if __name__ == "__main__":
    run_lstm_forecast("outputs/google_trends.csv", "ai tools")
