import csv
import os
from monotub.measurement import Measurement
from datetime import datetime
from monotub.dataSink import DataSink
import logging

logger = logging.getLogger(__name__)

class CSVLogger(DataSink):

    LOG_DIR = "logs"

    
    HEADER = [
        "timestamp",
        "millis",
        "humedad interior",
        "temperatura interior",
        #"humedad SHT41",
        #"temperatura SHT41",
        "humedad SCD41",
        "temperatura SCD41",
        "CO2 SCD41",
        "humedad exterior",
        "temperatura exterior",
    ]

    def __init__(self):

        self.current_file = None
        self.current_writer = None
        self.current_date = None

    def setup(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)
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
            self.current_writer.writerow(self.HEADER)

    def _rotate_log_if_needed(self):
        today = datetime.now().strftime("%Y-%m-%d")

        if today != self.current_date:
            self.current_file.close()
            self._open_log_file()

    def write(self, measurement: Measurement):
        self._rotate_log_if_needed()
        self.current_writer.writerow(measurement.to_csv_row())
        self.current_file.flush()

    def cleanup(self):
        if self.current_file:
            self.current_file.close()
