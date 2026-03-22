FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usar netcat en lugar de mysql para esperar
CMD ["sh", "-c", "echo 'Esperando a MySQL...'; while ! nc -z mysql-clientes 3306; do sleep 2; done; echo 'MySQL listo!'; uvicorn infrastructure.api.main:app --host 0.0.0.0 --port 8001 --reload"]