import csv
import os
from datetime import datetime
import logging
import serial

logger = logging.getLogger(__name__)

class AppCore:
    DEFAULT_PORT = "/dev/serial/by-id/usb-Arduino_LLC__www.arduino.cc__Genuino_Uno_9543231383735151E130-if00"
    DEFAULT_BAUDRATE = 9600
    LOG_DIR = "logs"

    def __init__(self, port):
        self.port = port
        self.serial_connection = None

        self.current_file = None
        self.current_writer = None
        self.current_date = None

    def _connect_serial(self):
        while True:
            try:
                logging.info(f"Connecting to {self.port}")

                self.serial_connection = serial.Serial(
                    self.port,
                    self.DEFAULT_BAUDRATE,
                    timeout=1,
                )

                logging.info("Connected")

                # Limpiar basura del buffer inicial
                self.serial_connection.reset_input_buffer()

                return

            except serial.SerialException as e:
                logging.error(
                    f"Failed to connect: {e}. "
                    "Retrying in 5 seconds..."
                )

                time.sleep(5)

    def setup(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)
        self._connect_serial()
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
                    "humedad interior",
                    "temperatura interior",
                    "humedad exterior",
                    "temperatura exterior",
                ]
            )

    def _rotate_log_if_needed(self):
        today = datetime.now().strftime("%Y-%m-%d")

        if today != self.current_date:
            self.current_file.close()
            self._open_log_file()

    def _process_line(self, line: str):
        try:
            millis, hum_int, temp_int, hum_ext, temp_ext  = line.split(",")

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            self.current_writer.writerow(
                [
                    timestamp,
                    millis,
                    hum_int,
                    temp_int,
                    hum_ext,
                    temp_ext,
                ]
            )

            self.current_file.flush()

            logging.info(
                f"{timestamp} "
                f"M={millis} "
                f"Hi={hum_int}% "
                f"Ti={temp_int}°C "
                f"H={hum_ext}% "
                f"T={temp_ext}°C"
            )

        except ValueError:
            logging.error(f"Invalid line: {line}")

    def run(self) -> int:
        self.setup()

        try:
            while True:
                self._rotate_log_if_needed()
                
                try:

                    line = (
                        self.serial_connection
                        .readline()
                        .decode(errors="ignore")
                        .strip()
                    )
                    
                except serial.SerialException:
                    logging.error("Lost serial connection")

                    try:
                        self.serial_connection.close()
                    except Exception:
                        pass

                    self._connect_serial()
                    continue

                if not line:
                    continue

                self._process_line(line)

        except KeyboardInterrupt:
            logging.info("\nStopping logger...")
            return 0

        finally:
            self.cleanup()

    def cleanup(self):
        if self.current_file:
            self.current_file.close()

        if self.serial_connection:
            self.serial_connection.close()