#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/../monotub_control" && pwd)"

DEFAULT_PORT="/dev/serial/by-id/usb-Arduino_LLC__www.arduino.cc__Genuino_Uno_9543231383735151E130-if00"
PORT="$DEFAULT_PORT"

FQBN="arduino:avr:uno"

COMPILE_ONLY=false

show_help() {
    cat << EOF
Usage:
    $(basename "$0") [options]

Options:
    -c, --compile-only
        Compile only. Do not upload.

    -p, --port <port>
        Serial port to use for upload.

    -h, --help
        Show this help message.

Examples:
    $(basename "$0")
        Compile and upload using the default port.

    $(basename "$0") -c
        Compile only.

    $(basename "$0") -p /dev/ttyACM1
        Compile and upload using /dev/ttyACM1.

    $(basename "$0") -c -p /dev/ttyACM1
        Compile only (port is ignored).
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--compile-only)
            COMPILE_ONLY=true
            shift
            ;;
        -p|--port)
            if [[ -z "$2" ]]; then
                echo "Error: missing port after $1"
                exit 1
            fi
            PORT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo
            show_help
            exit 1
            ;;
    esac
done

echo "🔧 Compiling..."
arduino-cli compile --fqbn "$FQBN" "$PROJECT_DIR"

if [[ "$COMPILE_ONLY" == true ]]; then
    echo "✅ Compile successful"
    exit 0
fi

echo "Using port: $PORT"

echo "🚀 Uploading..."
arduino-cli upload -p "$PORT" --fqbn "$FQBN" "$PROJECT_DIR"

echo "✅ Done"