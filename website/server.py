import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless plotting

from flask import Flask, render_template, send_file, make_response
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # <- required to enable 3D projection

import os
import traceback
from datetime import datetime, timedelta

app = Flask(__name__)
CSV_FILE = "voltage_data.csv"

# Function to generate and save the plot
def generate_plot():
    try:
        df = pd.read_csv(CSV_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        latest_time = df["timestamp"].max()
        cutoff_time = latest_time - timedelta(seconds=1)
        df = df[df["timestamp"] >= cutoff_time]

        if df.empty:
            print("[WARNING] No data available for plotting.")
            return

        signal = df["input_voltage_V"].values
        delay = 2
        X = signal[:-2*delay]
        Y = signal[delay:-delay]
        Z = signal[2*delay:]
        min_len = min(len(X), len(Y), len(Z))
        X, Y, Z = X[:min_len], Y[:min_len], Z[:min_len]

        # --- Layout: Time Series (top), Hysteresis (bottom left), Attractor (bottom right) ---
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle("Live Voltage Monitoring (Last 10 Seconds)", fontsize=16, color='orange')

        # Top: Time Series (Full Width)
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(df["timestamp"], df["input_voltage_V"], '-r', label="Input Voltage (V)")
        ax1.plot(df["timestamp"], df["measurement_voltage_V"], '-b', label="Measurement Voltage (V)")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Voltage (V)")
        ax1.set_title("Live Voltage Monitoring (Last 1s)")
        ax1.legend(loc="upper left")
        fig.autofmt_xdate()

        # Bottom Left: Phase Space
        ax2 = fig.add_subplot(2, 2, 3)
        ax2.scatter(df["input_voltage_V"], df["measurement_voltage_V"], c='black', s=10, alpha=0.7)
        ax2.set_xlabel("Input Voltage (V)")
        ax2.set_ylabel("Measurement Voltage (V)")
        ax2.set_title("Phase Space (Scatter)")
        ax2.grid(True)

        # Bottom Right: 3D Time-Delay Attractor
        ax3 = fig.add_subplot(2, 2, 4, projection='3d')
        ax3.scatter(X, Y, Z, c='black', s=3)
        ax3.set_title("3D Time-Delay Attractor")
        ax3.set_xlabel("x(t)")
        ax3.set_ylabel("x(t + t)")
        ax3.set_zlabel("x(t + 2t)")

        # Save and clean up
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/voltage_plot.png")

        if os.path.exists(output_path):
            os.remove(output_path)

        fig.savefig(output_path)
        plt.close(fig)

    except Exception as e:
        print(f"[ERROR] Failed to generate plot: {e}")

@app.route("/")
def index():
    generate_plot()
    return render_template("index.html")

@app.route("/plot")
def plot():
    generate_plot()
    response = make_response(send_file("static/voltage_plot.png", mimetype="image/png"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
