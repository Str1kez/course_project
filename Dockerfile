FROM python:3.10.5-slim as requirements

WORKDIR /temp

COPY pyproject.toml poetry.lock* /temp/

RUN pip install poetry

RUN poetry export -o requirements.txt --without-hashes

# Отвечает за создание среды
FROM python:3.10.5-slim as builder

RUN apt-get update; \
    apt-get install -y --no-install-recommends \ 
            libpq-dev \
            libc-dev \
            gcc;


# Отвечает за создание приложения

FROM builder AS build_app

WORKDIR /project

COPY --from=requirements /temp/requirements.txt requirements.txt

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app

RUN mkdir logs; \
    mkdir logs/app

WORKDIR /project/app

# это переопределено в docker-compose, так как нужна статика и миграции
CMD [ "python3", "app.py" ]
