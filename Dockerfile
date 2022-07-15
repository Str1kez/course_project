# Отвечает за создание среды
FROM python:3.10.5-slim as builder

RUN apt-get update; \
    apt-get install -y --no-install-recommends \ 
            libpq-dev \
            libc-dev \
            gcc;

COPY requirements.txt requirements.txt

RUN python3     -m pip install --upgrade pip; \
    pip3 install -r requirements.txt

# Отвечает за создание приложения

FROM builder AS build_app

WORKDIR /project

COPY . .

WORKDIR /project/app

# это переопределено в docker-compose, так как нужна статика и миграции
CMD [ "python3", "app.py" ]
