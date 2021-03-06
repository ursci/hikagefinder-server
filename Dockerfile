FROM python:3.8-alpine as builder

ENV APP_HOME /usr/src/hikage_finder

WORKDIR ${APP_HOME}

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv lock -r > requirements.txt


FROM python:3.8-alpine

ENV APP_HOME /usr/src/hikage_finder
ENV DOCKERIZE_VERSION v0.6.1

WORKDIR ${APP_HOME}
COPY --from=builder ${APP_HOME}/requirements.txt ./

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN apk add --no-cache --virtual build-deps \
    gcc \
    make \
    musl-dev \
 && apk add --no-cache --virtual run-deps \
    postgresql-dev \
 && pip install -r requirements.txt \
 && apk del --purge build-deps

COPY ./src ./src

WORKDIR ${APP_HOME}/src

EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
