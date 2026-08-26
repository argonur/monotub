import logging
import time
from opcua import Client, ua
from monotub.measurement import Measurement
from monotub.dataSink import DataSink

logger = logging.getLogger(__name__)

class OPCUAWriter(DataSink):

    OPC_ENDPOINT = "opc.tcp://192.168.1.99:4840"

    NODES = {
        "humidity_sht41": "ns=4;i=46",
        "temperature_sht41": "ns=4;i=47",
        "humidity_external": "ns=4;i=48",
        "temperature_external": "ns=4;i=49",
    }

    def __init__(self):

        self.client = None
        self.nodes = {}
    
    def setup(self):
        self._connect()

    def _connect(self):

        while True:

            try:

                logger.info(
                    f"Connecting to {self.OPC_ENDPOINT}"
                )

                self.client = Client(self.OPC_ENDPOINT)

                self.client.connect()

                self.nodes = {
                    name: self.client.get_node(node_id)
                    for name, node_id in self.NODES.items()
                }

                logger.info("Connected")

                return

            except Exception as e:

                logger.error(
                    f"Connection failed: {e}. "
                    "Retrying in 5 seconds..."
                )

                time.sleep(5)

    def _write_float(self, node, value):

        node.set_attribute(
            ua.AttributeIds.Value,
            ua.DataValue(
                ua.Variant(
                    float(value),
                    ua.VariantType.Float,
                )
            ),
        )

    def write(self, measurement: Measurement):

        try:
            
            for attribute, node in self.nodes.items():
                self._write_float(
                    node,
                    getattr(measurement, attribute)
                )

        except Exception as e:

            logger.error(f"Lost OPC UA connection: {e}")

            self.cleanup()

            self._connect()


    def cleanup(self):

        if self.client:

            try:
                self.client.disconnect()
            except Exception:
                pass