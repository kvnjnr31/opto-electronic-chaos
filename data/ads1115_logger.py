# ads_logger.py

import board
import busio
import time
import csv
import os
from datetime import datetime
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import pandas as pd
import matplotlib.pyplot as plt

SAMPLE_RATE = 860  # Hz
DURATION = 6    # seconds
CSV_FILE = "voltage_data.csv"
PLOT_PATH = os.path.join("alvi_web", "static", "voltage_plot.png")

class ADSLogger:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.ads.data_rate = SAMPLE_RATE
        self.channel1 = AnalogIn(self.ads, ADS.P1)
        self.channel2 = AnalogIn(self.ads, ADS.P2)

    def collect_data(self):
        print(f"[INFO] Collecting data for {DURATION} seconds at {SAMPLE_RATE} Hz...")
        data = []
        start_time = time.time()
        while time.time() - start_time < DURATION:
            elapsed = time.time() - start_time
            v1 = self.channel1.voltage
            v2 = self.channel2.voltage
            data.append([elapsed, v1, v2])
            time.sleep(1 / SAMPLE_RATE)
        print(f"[INFO] Data collection complete. {len(data)} samples recorded.")
        return data

    def save_to_csv(self, data):
        with open(CSV_FILE, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ElapsedTime", "Voltage_P1", "Voltage_P2"])
            writer.writerows(data)
        print(f"[INFO] Data saved to {CSV_FILE}")

    def generate_plot(self, data):
        df = pd.DataFrame(data, columns=["ElapsedTime", "Voltage_P1", "Voltage_P2"])
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.plot(df["ElapsedTime"], df["Voltage_P1"], '-r', label="Voltage P1")
        ax1.plot(df["ElapsedTime"], df["Voltage_P2"], '-b', label="Voltage P2")
        ax1.set_xlabel("Elapsed Time (s)")
        ax1.set_ylabel("Voltage (V)")
        ax1.set_title("Voltage vs Time")
        ax1.legend()

        ax2.scatter(df["Voltage_P1"], df["Voltage_P2"], color='k', alpha=0.8, s=8)
        ax2.set_xlabel("Voltage P1 (V)")
        ax2.set_ylabel("Voltage P2 (V)")
        ax2.set_title("Phase Plot: P1 vs P2")
        ax2.grid(True)

        plt.tight_layout()
        plt.savefig(PLOT_PATH)
        plt.close()
        print(f"[INFO] Plot saved to {PLOT_PATH}")

if __name__ == "__main__":
    logger = ADSLogger()
    data = logger.collect_data()
    logger.save_to_csv(data)
    logger.generate_plot(data)
