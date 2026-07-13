from monotub.dataSink import DataSink
from monotub.serialReader import SerialReader
from monotub.csvLogger import CSVLogger
from monotub.opcuaWriter import OPCUAWriter
import logging

logger = logging.getLogger(__name__)

class App:

    def __init__(self, port):

        self.serial_reader = SerialReader(port)
        
        self.data_sinks: list[DataSink] = [
            CSVLogger(),
            OPCUAWriter(),
        ]
    
    def setup(self):

        self.serial_reader.setup()
        for sink  in self.data_sinks:
            sink.setup()

    def cleanup(self):

        self.serial_reader.cleanup()
        for sink  in self.data_sinks:
            sink.cleanup()

    def run(self) -> int:

        self.setup()

        try:

            while True:

                measurement = self.serial_reader.read()

                if measurement is None:
                    continue

                for sink  in self.data_sinks:
                    sink.write(measurement)
        
        except KeyboardInterrupt:
        
            logger.info("Stopping application...")
            return 0
        
        except Exception:

            logger.exception("Unexpected error")
            return 1
        
        finally:
            self.cleanup()
