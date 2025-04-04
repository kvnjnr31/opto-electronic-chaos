# ads_logger.py

import board
import busio
import time
import csv
import os
from datetime import datetime
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class ADSLogger:
    def __init__(self, channel1=ADS.P1, channel2=ADS.P2, data_rate=860, duration=0, outfile="voltage_data.csv"):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.ads.data_rate = data_rate

        self.channel1 = AnalogIn(self.ads, channel1)
        self.channel2 = AnalogIn(self.ads, channel2)

        self.duration = duration  # 0 means run indefinitely
        self.outfile = outfile

    def read_once(self):
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "input_V": self.channel1.voltage,
            "measurement_V": self.channel2.voltage,
        }

    def run(self):
        print(f"Logging started... appending to {self.outfile}")
        file_exists = os.path.isfile(self.outfile)

        with open(self.outfile, mode="a", newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(["Timestamp", "Voltage_P0", "Voltage_P1"])

            start_time = time.time()
            last_print = start_time

            while True if self.duration == 0 else time.time() - start_time < self.duration:
                reading = self.read_once()
                writer.writerow([reading["timestamp"], reading["input_V"], reading["measurement_V"]])

                now = time.time()
                if now - last_print >= 1:
                    print("Logging...", end="\r")
                    last_print = now

                time.sleep(1 / self.ads.data_rate)

if __name__ == "__main__":
    logger = ADSLogger(duration=0, outfile="voltage_data.csv")
    logger.run()
