#!/usr/bin/env python3

import sys
import logging
import os

from core import AppCore

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

def main() -> int:
    port = (
        sys.argv[1] # main.py /dev/ttyACMX para especificar el puerto
        if len(sys.argv) > 1
        else AppCore.DEFAULT_PORT
    )
    core = AppCore(port)
    return core.run()


if __name__ == "__main__":
    sys.exit(main())