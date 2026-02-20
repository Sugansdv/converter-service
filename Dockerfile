FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-writer libreoffice-calc libreoffice-impress fonts-dejavu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180
