# PythonTemplate

Este repositorio es un "template" para proyectos de Python.

## Estructura del repositorio

```sh
    PythonTemplate/
    ├── .github
    │   ├── copilot-instructions.md
    │   └── workflows
    │       ├── daily_run.yml
    │       └── self_hosted.yml
    ├── .gitignore
    ├── .vscode
    │   └── settings.json
    ├── Dockerfile
    ├── README.md
    ├── docs
    │   ├── docker.md
    │   └── localActions.md
    ├── notes
    │   └── note.ipynb
    ├── pyproject.toml
    ├── requirements.txt
    ├── scripts
    │   ├── build_and_push_container.sh
    │   ├── setup_virtual_env.sh
    │   └── update_requirements.sh
    ├── src
    │   ├── __init__.py
    │   ├── core.py
    │   └── main.py
    └── tests
        ├── __init__.py
        └── test_core.py
```

<!--
Para generar el arbol ejecutar:
tree -a -I '.venv|.git'
-->

## Entorno virtual para Python

Se necesita un entorno virtual para instalar paquetes de Python. El script `setup_virtual_env.sh` puede usarse para recrear el entorno virtual. El archivo pyproject.toml es utilizado por ese script para instalar los paquetes necesarios. **Ejecuta el script de la siguiente manera**:

```sh
    . scripts/setup_virtual_env.sh
```

## VS Code: Virtual Environment automático

Este proyecto utiliza un virtual environment local en la carpeta `.venv`.

Para que VS Code use automáticamente este entorno, se recomienda el siguiente archivo `.vscode/settings.json`:

```json
{
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
"python.terminal.activateEnvironment": true
}
```

> ⚠️ **Nota**
>
> La primera terminal que abre VS Code puede no activar el virtual environment.
> Si esto ocurre, cierra la terminal y abre una nueva.

## Instalación de paquetes nuevos

Cada vez que se instala un paquete nuevo que sea necesario para correr la aplicación o para poder desarrollarla debe atualizarse el archivo `pyproject.toml`.

Para instalar un paquete y mostrar su version ejecuta:

```sh
    pip install paquete
    pip show paquete
```

Y con el nombre y la versión del paquete modificar el `pyproject.toml`.

## Requirements

El archivo `requirements.txt` es usado para crear un docker container que tenga instalados los paquetes necesarios para que pueda correr la aplicación. Cada que se instalen paquetes nuevos se tiene que actualizar este archivo antes de crear un nuevo contenedor. El script `update_requirements.sh` puede usarse para actualizar el archvo. **Ejecuta el script de la siguiente manera**:

```sh
    ./scripts/update_requirements.sh
```

## Crear y actualizar la versión en línea de un contenedor

Para crear y actualizar la versión en línea de un contenedor esta el script `build_and_push_container.sh`.

## Workflows

Se incluyen en este repo dos workflows muy simples `daily_run.yml` y `self_hosted.yml`. El primero está diseñado para correr en github, mientras que el segundo está pensado para correr de manera local usando `act`. Se incluye en la carpeta `docs` una descripción de como usar local actions (`localActions.md`).

## Como usar este repo

Para usar los archivos de este repo como base, ejecutar los siguientes comandos:

```sh
    mkdir proyecto_nuevo
    cp -a PythonTemplate/. proyecto_nuevo/
    cd proyecto_nuevo
    rm -rf .git
    git init
    git add .
    git commit -m "Initial commit: python template repo"
```

Create a repo *proyecto_nuevo* en Github y sube los archivos ejecutando los siguientes comandos:

```sh
    git remote add origin https://github.com/argonur/proyecto_nuevo.git
    git branch -M main
    git push -u origin main
```

¡Listo!
