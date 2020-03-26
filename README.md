# Shade Route API Server

## How to start the API server
### requirements
- Docker
- Docker Compose

### notice
This server uses 8000 port. Please don't forget to check the 8000 port is free.

### how to start the server
First, you have to prepare environment variables via `.env` file. This repository has a `example.env` file. You can create the `.env` file copying this file.

FIY, you can modify each values in `.env` file, especially `DB_PASS`.

```bash
$ cp example.env .env
$ vim .env
```

Then, you build a docker image and start containers (API server and PostGIS). After initializing PostGIS, you can see the API documentation on [http://localhost:8000/docs/](http://localhost:8000/docs/).

```bash
$ docker-compose build
$ docker-compose up -d
```

## How to develop the API server
### requirements
- Docker
- Docker Compose
- Python 3.8
- pipenv

### install developing requirements
Example on macOS.

```bash
$ brew install python@3.8 pipenv
```

### create virtual python environment and install packages
We create a virtual python environment with `pipenv`. This repository has a `Pipfile` and `Pipfile.lock`. So you can reproduce the virtual python environment on your computer.

```bash
$ pipenv install -d  # install required packages
$ pipenv shell  # enable virtual python environment
```

### how to start the API server
See above secton. Changes on your code will be applied automatically on the docker container without rebuilding or restarting.

### how to run linter
On this repository, the Gitlab CI has been enabled. When you push a commit on this repository, the CI checks code format automatically. If your code doesn't follow the code formatting rule, the CI will send a error to you. Before pushing the commits, you can re-format the codes with linter.

```bash
$ pipenv run fmt
```
