# Monotub Control Guide

## arduino-cli

### Instalacion

```sh
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
arduino-cli config init
arduino-cli core update-index
arduino-cli core install arduino:avr
sudo mv ~/bin/arduino-cli /usr/local/bin/
```

✅ Verifica

```sh
arduino-cli version
```

Si ves algo como:

```sh
arduino-cli  Version: 1.5.0
```

→ ya quedó bien integrado en el sistema

### Identificación del Arduino mediante alias persistente

Para detectar automáticamente la tarjeta Arduino conectada, primero puede utilizarse el siguiente comando:

```bash
arduino-cli board list
```

Ejemplo de salida:

```text
Port         Protocol Type              Board Name      FQBN            Core
/dev/ttyACM0 serial   Serial Port (USB) Arduino Uno    arduino:avr:uno arduino:avr
```

Aunque `/dev/ttyACM0` permite la comunicación con la tarjeta, este nombre puede cambiar entre reinicios o al conectar otros dispositivos USB.

Para obtener un identificador persistente asociado al dispositivo, se recomienda utilizar:

```bash
ls -l /dev/serial/by-id/
```

Ejemplo de salida:

```text
usb-Arduino_LLC_Arduino_Uno_8543932393535180E1D1-if00 -> ../../ttyACM0
```

El enlace simbólico dentro de `/dev/serial/by-id/` es estable y está basado en la identidad del dispositivo USB, por lo que puede utilizarse directamente en la aplicación:

```text
/dev/serial/by-id/usb-Arduino_LLC_Arduino_Uno_8543932393535180E1D1-if00
```

Usar este alias en lugar de `/dev/ttyACM0` evita problemas cuando el sistema asigna nombres diferentes a los puertos serie después de una reconexión o reinicio.

### 🚀 Compilar y subir

```sh
arduino-cli compile --fqbn arduino:avr:uno tu_proyecto

arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno tu_proyecto
```

## logging

En la aplicación que corre en la RasPi se decidió usar el módulo logging para generar mensajes que indiquen el estatus de la aplicación y posibles causas de error. Además como la aplicación correrá como un servicio que inicia de forma automática, los mensajes quedan grabados en el buffer que se puede revisar con `journalctl`.

Por default, en main.py, está definido que el nivel mínimo de mensajes que serán loggeados será "INFO".

```python
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
```

Sin embargo este nivel puede cambiarse, ya sea seteando una variable de estado persistente, por ejemplo así:

```bash
echo 'export LOG_LEVEL=INFO' >> ~/.bashrc
```

o iniciando la aplicación de la siguiente manera, para que setear el nivel solo para esa ejecución:

```bash
LOG_LEVEL=DEBUG python main.py
```

### Para servicios systemd (recomendado)

Ponlo directamente en el `.service`:

```bash
[Service]
Environment=LOG_LEVEL=INFO
```

Luego:

```bash
sudo systemctl daemon-reload
sudo systemctl restart monotub-logger.service
```

Esto:

- Sobrevive reinicios.
- Es específico para ese servicio.
- No contamina el entorno de otros programas.

#### Alternativa más limpia: archivo .env

Por ejemplo:

```bash
nano /home/r2d2/github/monotub/.env
```

Contenido:

```bash
LOG_LEVEL=INFO
```

Luego en el servicio:

```bash
[Service]
EnvironmentFile=/home/r2d2/github/monotub/.env
```

Después:

```bash
sudo systemctl daemon-reload
sudo systemctl restart monotub-logger.service
```

Ventajas:

- No editas el .service cada vez.
- Puedes agregar más configuración:

```bash
LOG_LEVEL=INFO
SERIAL_PORT=/dev/serial/by-id/...
CSV_DIR=/home/r2d2/logs
```

## Correr python App como servicio (systemd)

Esto es lo que realmente hará que no tengas que tocar nada.

Supongamos esta estructura:

```bash
/home/r2d2/github/monotub/logger/
├── main.py
├── core.py
└── logs/
```

Prueba primero:

```bash
cd /home/r2d2/github/monotub/logger

python3 main.py
```

Asegúrate de que funciona.

### Crear el servicio

```bash
sudo nano /etc/systemd/system/monotub-logger.service
```

Contenido:

```bash
[Unit]
Description=Monotub Logger
After=network.target

[Service]
Type=simple

User=r2d2
WorkingDirectory=/home/r2d2/github/monotub/logger

ExecStart=/usr/bin/python3 /home/r2d2/github/monotub/logger/main.py

Restart=always
RestartSec=10

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Activarlo

Recargar servicios:

```bash
sudo systemctl daemon-reload
```

Habilitar para que inicie al arrancar:

```bash
sudo systemctl enable monotub-logger.service
```

Iniciarlo ahora:

```bash
sudo systemctl start monotub-logger.service
```

### Verificar que funciona

Estado:

```bash
sudo systemctl status monotub-logger.service
```

Ver logs:

```bash
journalctl -u monotub-logger.service -f
```

Esto es equivalente a hacer:

```bash
tail -f
```

pero sobre el logger del sistema.

### Comandos útiles

Detener:

```bash
sudo systemctl stop monotub-logger.service
```

Reiniciar:

```bash
sudo systemctl restart monotub-logger.service
```

Deshabilitar el arranque automático:

```bash
sudo systemctl disable monotub-logger.service
```

## Journaling para ver logs del servicio

`journalctl -u monotub-logger.service -f` te permite **ver en tiempo real la salida de tu servicio**, como si estuvieras ejecutando el script manualmente en una terminal.

Desglosemos el comando:

```bash
journalctl -u monotub-logger.service -f
```

### `journalctl`

Es la herramienta para consultar el **journal de systemd**, que es el sistema de logs de Linux.

Piensa en él como una base de datos central donde se guarda:

- Logs del kernel
- Logs de servicios (`systemd`)
- Mensajes del sistema
- Salidas `stdout` y `stderr` de tus programas

`-u monotub-logger.service`

Filtra por unidad de systemd (`unit`).

Es decir:

> "Muéstrame únicamente los logs generados por el servicio `monotub-logger.service.`"

Sin `-u`, verías logs de todo el sistema.

`-f`

Significa follow, igual que en:

```bash
tail -f archivo.log
```

Es decir:

> "Quédate esperando y muéstrame nuevas líneas conforme aparezcan."

### ¿Para qué sirve?

Es extremadamente útil para depuración.

Por ejemplo, si el Arduino se desconecta y tienes:

```python
logger.error(f"Invalid line: {line}")
```

verías inmediatamente algo así, por ejemplo:

```bash
Jun 11 08:47:20 R2D2-3BP main.py[4571]: 2026-06-11 08:47:20,209 core ERROR Invalid line: Error: No se puede leer el sensor DHT exterior. Revisa las conexiones.
```

Sin tener que detener el servicio ni conectarte a la consola del programa.

### Otros comandos útiles

Ver todos los logs anteriores:

```bash
journalctl -u monotub-logger.service
```

Ver solo las últimas 50 líneas:

```bash
journalctl -u monotub-logger.service -n 50
```

Ver logs desde el último arranque:

```bash
journalctl -u monotub-logger.service -b
```

Ver logs de hoy:

```bash
journalctl -u monotub-logger.service --since today
```

### Uso del journal

Yo usaría el journal principalmente para:

- Verificar que el servicio arrancó correctamente.
- Diagnosticar problemas si deja de registrar datos.
- Revisar si hubo desconexiones del Arduino.

Una vez que el sistema esté estable, probablemente lo consultarás muy poco. Pero cuando algo falle, será de las primeras cosas que revisarás.
