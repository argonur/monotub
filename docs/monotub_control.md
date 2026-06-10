# Monotub Control Guide

## arduino-cli

### instalacion

curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
arduino-cli config init
arduino-cli core update-index
arduino-cli core install arduino:avr
sudo mv ~/bin/arduino-cli /usr/local/bin/

✅ Verifica

arduino-cli version

Si ves algo como:

arduino-cli  Version: 1.5.0

→ ya quedó bien integrado en el sistema

### Detección

arduino-cli board list

/dev/ttyACM0 arduino:avr:uno

### 🚀 Compilar y subir

arduino-cli compile --fqbn arduino:avr:uno tu_proyecto

arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno tu_proyecto

