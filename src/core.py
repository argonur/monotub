import csv
import os
from datetime import datetime

import serial


class AppCore:
    DEFAULT_PORT = "/dev/serial/by-id/usb-Arduino_LLC__www.arduino.cc__Genuino_Uno_9543231383735151E130-if00"
    DEFAULT_BAUDRATE = 9600
    LOG_DIR = "logs"

    def __init__(self):
        self.serial_connection = None

        self.current_file = None
        self.current_writer = None
        self.current_date = None

    def setup(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)

        self.serial_connection = serial.Serial(
            self.DEFAULT_PORT,
            self.DEFAULT_BAUDRATE,
            timeout=1,
        )

        self._open_log_file()

    def _open_log_file(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")

        filename = os.path.join(
            self.LOG_DIR,
            f"{self.current_date}.csv",
        )

        file_exists = os.path.isfile(filename)

        self.current_file = open(
            filename,
            mode="a",
            newline="",
        )

        self.current_writer = csv.writer(self.current_file)

        if not file_exists:
            self.current_writer.writerow(
                [
                    "timestamp",
                    "millis",
                    "temperatura exterior",
                    "humedad exterior",
                    "temperatura interior",
                    "humedad interior",
                ]
            )

    def _rotate_log_if_needed(self):
        today = datetime.now().strftime("%Y-%m-%d")

        if today != self.current_date:
            self.current_file.close()
            self._open_log_file()

    def _process_line(self, line: str):
        try:
            millis, temp_ext, hum_ext, temp_int, hum_int = line.split(",")

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            self.current_writer.writerow(
                [
                    timestamp,
                    millis,
                    temp_ext,
                    hum_ext,
                    temp_int,
                    hum_int
                ]
            )

            self.current_file.flush()

            print(
                f"{timestamp} "
                f"M={millis} "
                f"T={temp_ext}°C "
                f"H={hum_ext}% "
                f"Ti={temp_int}°C "
                f"Hi={hum_int}%"
            )

        except ValueError:
            print(f"Invalid line: {line}")

    def run(self) -> int:
        self.setup()

        try:
            while True:
                self._rotate_log_if_needed()

                line = (
                    self.serial_connection
                    .readline()
                    .decode(errors="ignore")
                    .strip()
                )

                if not line:
                    continue

                self._process_line(line)

        except KeyboardInterrupt:
            print("\nStopping logger...")
            return 0

        finally:
            self.cleanup()

    def cleanup(self):
        if self.current_file:
            self.current_file.close()

        if self.serial_connection:
            self.serial_connection.close()