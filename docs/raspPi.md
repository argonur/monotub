# RasPI 

## Desactivar GUI

### Opción 1 (rápida): desactivar la GUI (suficiente en la mayoría de casos)

No necesitas reinstalar. Puedes dejar tu sistema actual y simplemente evitar que arranque el entorno gráfico.

Ejecuta:

```sh
sudo raspi-config
```

Luego:

- `System Options`
- `Boot / Auto Login`
- Selecciona: **Console** (no Desktop)

Reinicias:

```sh
sudo reboot
```

Con eso:

- Arranca en terminal
- La GUI no se levanta automáticamente
- Sigues teniendo todo instalado por si lo necesitas

#### Iniciar la GUI manualmente una sola vez

Desde la terminal:

```sh
startx
```

Esto inicia el entorno gráfico para esa sesión.

## IP estática

### 🧠 Opción 1 (la mejor): IP fija desde el router (DHCP reservation)

👉 Esta es la forma profesional.

Tu router le asigna **siempre la misma IP** a tu Raspberry Pi 3 Model B+ usando su MAC address.

#### Cómo hacerlo

1. En la RasPi, obtén la MAC:

```sh
ip a
```

Busca algo como:

```sh
link/ether b8:27:eb:xx:xx:xx
```

2. Entra a tu router (normalmente):

- `192.168.0.1`
- o `192.168.1.1`

3. Busca algo tipo:

- **DHCP Reservation**
- **Static Lease**
- **LAN Settings**

4. Agrega:

- MAC address de la RasPi
- IP fija (ej: `192.168.1.50`)

#### Ventajas

- No rompes configuración interna
- Evitas conflictos de IP
- Funciona mejor con redes grandes o cambiantes

👉 Si tienes acceso al router, usa esta. Sin discusión.

### ⚙️ Opción 2: IP estática en la RasPi

👉 Útil si NO puedes tocar el router.

Edita:

```sh
sudo nano /etc/dhcpcd.conf
```

Al final agrega algo así:

```sh
interface wlan0
static ip_address=192.168.1.50/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 1.1.1.1
```

O si usas cable:

```sh
interface eth0
static ip_address=192.168.1.50/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8 1.1.1.1
```

Reinicias:

```sh
sudo reboot
```

## Prueba rápida sin Python para validar conexión serial

Instala:

```sh
sudo apt install screen
```

Luego:

```sh
screen /dev/ttyACM0 9600
```

Si ves los datos → todo está correcto

Salir de screen:

```sh
Ctrl + A, luego K
```
