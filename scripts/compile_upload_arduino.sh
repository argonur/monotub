#!/usr/bin/env bash

set -e  # falla si algo truena

PROJECT_DIR="$(cd "$(dirname "$0")/../monotub_control" && pwd)"
#PORT="${1:-/dev/ttyACM0}" # uso  ./scripts/build_upload.sh /dev/ttyACM1
PORT="/dev/serial/by-id/usb-Arduino_LLC__www.arduino.cc__Genuino_Uno_9543231383735151E130-if00"
FQBN="arduino:avr:uno"

echo "🔧 Compiling..."
arduino-cli compile --fqbn "$FQBN" "$PROJECT_DIR"

echo "Using port: $PORT"

echo "🚀 Uploading..."
arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$PROJECT_DIR"

echo "✅ Done"