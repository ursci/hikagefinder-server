# Hikage Finder API Server

## How to start the API server

### Requirements
- Docker
- Docker Compose

### Notice
This server uses 8000 port. Please don't forget to check the 8000 port is free.

### How to start the server
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

### Requirements
- Docker
- Docker Compose
- Python 3.8
- pipenv

### Install developing requirements
Example on macOS:

```bash
$ brew install python@3.8 pipenv
```

Example on Ubuntu:
```bash
$ sudo apt install pipenv
```

### Create virtual python environment and install packages
We create a virtual python environment with `pipenv`. This repository has a `Pipfile` and `Pipfile.lock`. So you can reproduce the virtual python environment on your computer.

```bash
$ pipenv install -d  # install required packages
$ pipenv shell  # enable virtual python environment
```

### How to start the API server
See above section. Changes on your code will be applied automatically on the docker container without rebuilding or restarting.

### How to run linter
On this repository, the Gitlab CI has been enabled. When you push a commit on this repository, the CI checks code format automatically. If your code doesn't follow the code formatting rule, the CI will send a error to you. Before pushing the commits, you can re-format the codes with linter.

```bash
$ pipenv run fmt
```

### How to import original shape file data
First, you convert a shape file into a sql file with this command. To run this command, you have to make a `tmp` directory which includes shape files. 

```bash
$ mkdir -p tmp
$ cp foo.shp foo.dbf (and other related files) ./tmp
$ docker container run -it --rm --volume ${PWD}/tmp:/data pgrouting/pgrouting:13-3.0-3.1.1 bash
# apt update 
# apt install -y postgis
# cd /data
# shp2pgsql -D -I -S -a -s 4326 path/to/foo.shp public.import > import.sql
```

Alternatively download sample data:

```bash
wget -O data/import.sql https://raw.githubusercontent.com/ursci/hikagefinder-data/main/shibuya/SunExpo_shibuya_9_10_every5min.sql
```

Then create and setup the database where necessary: 

```bash
$ createdb -U postgres hikage_prod
$ psql -U postgres -d hikage_prod -f setup/00_create_role.sql
$ psql -U postgres -d hikage_prod -f setup/01_enable_extensions.sql
$ psql -U postgres -d hikage_prod -f setup/02_prepare_tables.sql
$ psql -U postgres -d hikage_prod -f setup/03_prepare_views.sql
$ psql -U postgres -d hikage_prod -f setup/04_insert_shortest_function.sql
$ psql -U postgres -d hikage_prod -f setup/05_insert_shade_function.sql
```

In the next step import and process the converted data:

```bash
$ docker-compose exec postgis bash
# psql -U ursci -d hikage_prod -f data/import.sql
# psql -U ursci -d hikage_prod -c "SELECT public.pgr_createTopology('import', 0.0000001, 'geom', 'gid')";
# psql -U ursci -d hikage_prod -c "REFRESH MATERIALIZED VIEW public.shades"
# psql -U ursci -d hikage_prod -c "ANALYZE"
```

Finally, you just run the docker containers above way.

## Memo

## Run in Local Environment
Steps to do to run application in a local environment.

* Install `pipenv`, for example with `sudo apt install pipenv` or `brew install pipenv`
* Install dependencies with `pipenv install` 
* Activate the virtual environment with `pipenv shell`
* Run the application with `uvicorn main:app --host 0.0.0.0 --reload`
* Leave the virtual environment with `exit`

Configure PyCharm to run/debug the application

* Create a new Configuration: `Run->Edit Configurations`
* Set the Script Path to `uvicorn`
* Set the Parameters to `main:app --host 0.0.0.0 --reload`
* Set the Python Interpreter to `venv/bin/python`
* Set the Working Directory to  `src`
