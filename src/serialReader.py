from datetime import datetime
from measurement import Measurement
import logging
import serial
import time

logger = logging.getLogger(__name__)

class SerialReader:
    DEFAULT_PORT = "/dev/serial/by-id/usb-Arduino_LLC__www.arduino.cc__Genuino_Uno_9543231383735151E130-if00"
    DEFAULT_BAUDRATE = 9600

    def __init__(self, port):
        self.port = port
        self.serial_connection = None

    def _connect_serial(self):
        while True:
            try:
                logger.info(f"Connecting to {self.port}")

                self.serial_connection = serial.Serial(
                    self.port,
                    self.DEFAULT_BAUDRATE,
                    timeout=1,
                )

                logger.info("Connected")

                # Limpiar basura del buffer inicial
                self.serial_connection.reset_input_buffer()

                return

            except serial.SerialException as e:
                logger.error(
                    f"Failed to connect: {e}. "
                    "Retrying in 5 seconds..."
                )

                time.sleep(5)

    def setup(self):
        self._connect_serial()

    def _process_line(self, line: str) -> Measurement | None:
        try:
            (
                millis,
                hum_int,
                temp_int,
                hum_sht41,
                temp_sht41,
                hum_ext,
                temp_ext,
            ) = line.split(",")

            measurement = Measurement(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                millis=int(millis),

                humidity_internal=float(hum_int),
                temperature_internal=float(temp_int),

                humidity_sht41=float(hum_sht41),
                temperature_sht41=float(temp_sht41),

                humidity_external=float(hum_ext),
                temperature_external=float(temp_ext),
            )

            logger.debug(
                f"{measurement.timestamp} "
                f"M={measurement.millis} "
                f"Hi={measurement.humidity_internal:.1f}% "
                f"Ti={measurement.temperature_internal:.1f}°C "
                f"Hs={measurement.humidity_sht41:.1f}% "
                f"Ts={measurement.temperature_sht41:.1f}°C "
                f"He={measurement.humidity_external:.1f}% "
                f"Te={measurement.temperature_external:.1f}°C"
            )

            return measurement

        except ValueError:
            logger.error(f"Invalid line: {line}")
            return None

    def read(self) -> Measurement | None:
        try:
            line = (
                self.serial_connection
                .readline()
                .decode("utf-8")
                .strip()
            )

            if not line:
                return None

            return self._process_line(line)

        except serial.SerialException:
            logger.exception("Serial connection lost")
            self.cleanup()
            self._connect_serial()
            return None        

    def cleanup(self):
        if self.serial_connection:
            self.serial_connection.close()