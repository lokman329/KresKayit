FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY  . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "app.py"]