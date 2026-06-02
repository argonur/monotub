# Uso de Docker y Docker images en el workflow de GitHub

## Creación de un repositorio

Ir a <https://hub.docker.com/repositories/> y crear un repositorio.

1. Asignarle un nombre
2. Dar una breve descripción de las imagenes que contiene el repositorio
3. Elegir si el repositorio va a ser público o privado.

## Creacion de una imagen

Para crear una imagen ejecutar el sig. comando desde la ubicación donde se encuentre el `Dockerfile`:

```sh
docker build -t usuario/repositorio:tag .
```

## Signing in to Docker from WSL

Para poder subir la imagen al repositorio es necesario acceder a Docker desde WSL o desde cualquier CLI. Para poder acceder, es necesario ir a <https://app.docker.com/accounts/usuario/settings/account-information> y en *Personal access tokens* crear un token.

1. Dar una descripción, por ejemplo que indique donde se va a usar
2. Elegir *None* como fecha de expiración
3. Dar permisos Read/Write/Delete 
4. Dar click en *Generate*

Guardar el token generado, ya que no se podrá volver a mostrar.

Accder a Docker en WSL de la siguiente manera:

```sh
docker login -u username
Password: PersonalToken
```

## Subir la imagen a un repositorio

Para subir la imagen al repositorio

```sh
docker push usuario/repositorio:tag
```

## Uso de la imagen en el workflow de Github

En la carpeta .github/workflows se encuentran los archivos *yml* que contienen la descripción de los worflows. Para indicar que imagen se usará modificar la linea *image*.

```yml
jobs:
  Job1:
    runs-on: [self-hosted, local]
    container:
      image: usuario/repositorio:tag
```
