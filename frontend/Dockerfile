FROM python:3.11-slim

# Instalar Node.js (necesario para Reflex)
RUN apt-get update && apt-get install -y curl unzip
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Inicializar reflex y preparar producción
RUN reflex init

# Exponer el puerto del frontend (3000) y de la API de Reflex (8000)
EXPOSE 3000 8000

# El comando en producción para Reflex con API_URL configurada
CMD ["reflex", "run", "--env", "prod", "--frontend-port", "3000", "--backend-port", "8000"]