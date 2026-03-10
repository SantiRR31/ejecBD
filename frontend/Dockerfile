FROM python:3.11-slim

# Instalar Node.js (necesario para Reflex)
RUN apt-get update && apt-get install -y curl unzip
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && apt-get install -y nodejs

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
# Inicializar reflex
#RUN reflex init

# Exponer el puerto del frontend y del backend interno de Reflex
EXPOSE 3000
CMD ["reflex", "run", "--env", "prod"]