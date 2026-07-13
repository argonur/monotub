#!/usr/bin/env python3

import sys
import logging
import os

from monotub.serialReader import SerialReader
from monotub.app import App

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

logging.getLogger("opcua").setLevel(logging.WARNING)

def main() -> int:
    port = (
        sys.argv[1] # main.py /dev/ttyACMX para especificar el puerto
        if len(sys.argv) > 1
        else SerialReader.DEFAULT_PORT
    )
    
    app = App(port)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())