from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Measurement:
    timestamp: datetime
    millis: int

    humidity_internal: float
    temperature_internal: float

    humidity_sht41: float
    temperature_sht41: float

    humidity_external: float
    temperature_external: float

    def to_csv_row(self):
        return [
            self.timestamp,
            self.millis,
            self.humidity_internal,
            self.temperature_internal,
            self.humidity_sht41,
            self.temperature_sht41,
            self.humidity_external,
            self.temperature_external,
        ]
