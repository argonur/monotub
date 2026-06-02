FROM python:3.12-slim-bookworm

#PYTHONUNBUFFERED=1: Desactiva el buffering de stdout/stderr, lo que es crucial para:
#    Ver logs en tiempo real en contenedores Docker
#    Evitar problemas con la salida en sistemas de logging
#    Mejorar el rendimiento en entornos de producción
#PYTHONDONTWRITEBYTECODE=1: Previene la creación de archivos .pyc:
#    Reduce el tamaño de la imagen final
#    Evita problemas de caché con bytecode en entornos efímeros
#    Mejora la consistencia en despliegues
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

#Copiar requirements.txt e instalar dependencias Python
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

CMD ["bash"]