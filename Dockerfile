FROM python:3.8-alpine as builder

ENV APP_HOME /usr/src/shade_route_api

WORKDIR ${APP_HOME}

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv lock -r > requirements.txt


FROM python:3.8-alpine

ENV APP_HOME /usr/src/shade_route_api

WORKDIR ${APP_HOME}
COPY --from=builder ${APP_HOME}/requirements.txt ./

RUN apk add --no-cache --virtual build-deps \
    gcc \
    make \
    musl-dev \
    postgresql-dev \
 && pip install -r requirements.txt \
 && apk del --purge build-deps

COPY ./src ./src

WORKDIR ${APP_HOME}/src

EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
