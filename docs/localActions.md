# Configuración e instalación de `act`

`act` es una herramienta que te permite ejecutar GitHub Actiones directamente en tu máquina local.

## Ventajas

1. Retroalimentación rápida (Fast Feedback Loop)
    - Acelera el desarrollo y la depuración. Puedes ejecutar tu flujo de
      trabajo inmediatamene, el lugar de commit-push-waid-debug
    - Reduce la dependencia de GitHub: No necesitas enviar cada cambio a tu
      repositorio remoto para ver si tu flujo de trabajo funciona.

2. Ejecutor de Tareas Local (Local Task Runner)
    - Consolidación de tareas: Puedes definir tus procesos de compilación,
      prueba y luego ejecutarlos con act.
    - Consistencia

3. Simulación del entorno GitHub Actions

## Instalación

1. Instalación mediante el script de bash:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

**NOTA** El binario `act` se guarda  por defecto en el directorio `~/bin/`. Este directorio debe de estar en la variable de entorno `$PATH` del sistema, checar con: 

```shell
echo $PATH
```

en caso de que no esté modificarlo en `.profile`. Opcionalmente puede mover el binario a al directorio `.local/bin/`

2. Necesitas tener Docker instalado y ejecutándose en tu sistema Linux para que
   act funcione correctamente. Esto se debe a que act ejecuta los trabajos de
GitHub Actions dentro de contenedores Docker.  
    - Instala Docker
    - Asegurate de que se esté ejecutando con el gestor de servicios systemctl:

```shell
sudo systemctl status docker
```

  si está en modo `active (running)` está listo para usarse.

## Tu Proyecto y Flujos de Trabajo

Para usar act, necesitas un proyecto con un directorio .github/workflows que contenga tus archivos .yml de GitHub Actions, igual que si los fueras a subir a GitHub.

Ahora desde la raíz de tu proyecto ejecuta:

```shell
act
```

La primera vez que ejecutes act, te preguntará qué imagen de Docker quieres usar para el runner ubuntu-latest. Generalmente, act te ofrecerá opciones. Aparece algo así

```shell
? Choose the default image you want to use for 'ubuntu-latest' [Use arrows to move, type to filter]
  [Use 'tiny' (300MB) for GitHub Actions]
  [Use 'medium' (1.2GB) for GitHub Actions]
  [Use 'large' (4.5GB) for GitHub Actions]
```

Las más comunes son tiny o medium. `act` descargará la image de Docker y ejecutará cada paso de tu flujo de trabajo mostrando la salida en tu terminal.

## Opciones avanzadas de act

### Pasar secretos de github

Si nuestro archivo yml contiene secretos, por ejemplo, si en nuestro yml aparece

```yml
env:
PolygonKey: ${{ secrets.POLYGONKEY }}
```

Podemos pasar el secreto con:

```shell
act -s POLYGONKEY="122jkdkjjd" 
```

o múltiples secretos con 

```shell
act -s POLYGONKEY="122jkdkjjd" -s ALPHAVANTAGEKEY="QNBsaskkdkdF"
```

alternativamente podemos almacenar estas claves en un archivo, por ejemplo, guardamos las claves anteriores en el archivo que llamaremos `secrets` hubicado en algún directorio (no necesariamente del proyecto) 

```shell
POLYGONKEY="ashlskakjdjksaksjkjs"
ALPHAVANTAGEKEY="QNBsaskkdkdF"
```

y los mandamos a llamar con el el flag `--secret-file`:

```shell
    act --secret-file <path/screts>
```

### Cambiar de runner

Podemos especificar que tipo de imagen de Docker usar, por ejemplo, si en nuestro yaml aparece:

```shell
runs-on: ubuntu-latest
```

Podemos especificar en las opciones de `act` la imagen que tengas instalado en Docker que queremos usar mediante el flag `-P`. Ejemplo:

```shell
act -P ubuntu-latest=catthehacker/ubuntu:act-18.04
```

  las imagenes tienen que aparecer en la lista de `docker images`. El repositorio de act ya tiene algunos contenedores que podemos usar para correr nuestros runners locales
  vea `https://nektosact.com/usage/runners.html` para ver los disponibles.

Para más funcionalidades vea  el manual `https://nektosact.com/usage/index.html`

**Nota** No necesitamos hacer commits para probar los cambios en el repositorio.

## Integración con VSCODE

VSCODE tiene una extensión que integra `docker` con `act` que se llama `GitHub Local Actions`. Aunque la documentación del complemento no lo indica, al parecer se tiene mejor integración con los secrets si se abre sesión de github con el complemento de vscode. Si abrimos el panel lateral del plugin, tenemos que verificar que los componentes: `nektos/act` y `Docker engine` estén instalados y activos. Los secrets se pueden editar directamente en el apartado de `SETTINGS` del plugin.
