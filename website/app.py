
from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CSV_FILE = "voltage_data.csv"

# Function to generate and save the plot
def generate_plot():
    try:
        df = pd.read_csv(CSV_FILE)

        # Convert timestamp to datetime
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        # Keep only the last 0.5 seconds of data
        latest_time = df["Timestamp"].max()
        cutoff_time = latest_time - timedelta(seconds=0.5)
        df = df[df["Timestamp"] >= cutoff_time]

        if df.empty:
            print("[WARNING] No data available for plotting.")
            return

        # --- Time Series Plot ---
        plt.figure(figsize=(10, 5))
        plt.plot(df["Timestamp"], df["Voltage_P0"], '-r', label="Voltage P0 (V)")
        plt.plot(df["Timestamp"], df["Voltage_P1"], '-b', label="Voltage P1 (V)")
        plt.xlabel("Time")
        plt.ylabel("Voltage (V)")
        plt.legend(loc="upper left")
        plt.title("OPA380 Live Voltage Monitoring (Last 0.5s)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("static/voltage_plot.png")
        plt.clf()

        # --- Phase Space Plot (P0 vs P1) ---
        plt.figure(figsize=(5, 5))
        plt.plot(df["Voltage_P0"], df["Voltage_P1"], 'k-', alpha=0.8)
        plt.xlabel("Voltage P0 (V)")
        plt.ylabel("Voltage P1 (V)")
        plt.title("Phase Space (P0 vs P1)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("static/phase_plot.png")
        plt.clf()
        plt.close()

    except Exception as e:
        print(f"[ERROR] Failed to generate plot: {e}")

@app.route("/")
def index():
    generate_plot()
    return render_template("index.html")

@app.route("/plot")
def plot():
    generate_plot()
    return send_file("static/voltage_plot.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
