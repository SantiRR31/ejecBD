# Usamos una imagen ligera de Python 3.11
FROM python:3.11-slim

# Evitar que Python genere archivos .pyc y asegurar salida en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema
# - mariadb-client: Necesario para ejecutar 'mariadb-dump'
# - libmariadb-dev y gcc: Necesarios para instalar el driver 'mysqlclient' de Python
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del backend
COPY . .

# Exponer el puerto de Flask
EXPOSE 5000

# Comando para arrancar la aplicación
CMD ["python", "app.py"]