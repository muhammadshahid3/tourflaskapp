FROM python:3.12-slim

WORKDIR /app

# System deps needed to build PyMySQL's cryptography dependency
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/app/static/images/uploads

EXPOSE 5000

ENV FLASK_APP=run.py

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "run:app"]
