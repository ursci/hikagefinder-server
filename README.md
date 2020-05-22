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

### how to import shape file
First, you convert a shape file into a sql file with this command. To run this command, you have to make a `shape_files` directory which includes shape files. 

```bash
$ mkdir shape_files
$ cp foo.shp foo.dbf (and other related files) shape_files
$ docker container run -it --rm --volume ${PWD}/shape_files:/shape_files pgrouting/pgrouting:12-3.0-master bash
# apt update
# apt install -y postgis
# cd /shape_files
# shp2pgsql -D -I -s 4612 SunExpo_shibuya_9_10_every5min.shp shade > SunExpo_shibuya_9_10_every5min.sql
```

Then, import the sql file into our database. Before importing, you have to add a line to the sql file.

```bash
$ vim ./shape_files/SunExpo_shibuya_9_10_every5min.sql
```

```sql
SET CLIENT_ENCODING TO UTF8;
SET STANDARD_CONFORMING_STRINGS TO ON;
BEGIN;
CREATE EXTENSION postgis;  -- ADD THIS LINE ON LINE 4
CREATE EXTENSION pgrouting; -- ADD THIS LINE ON LINE 5
CREATE TABLE "shade" (gid serial,
```

Copy the sql file as initialize script.

```bash
$ cp ./shape_files/SunExpo_shibuya_9_10_every5min.sql ./initial_sql/01_import_shade_rates.sql
```

Finally, you just run the docker containers above way.

## Memo
### How to insert flatten data

```sql
CREATE TABLE shibuya_roads (id integer primary key, geom geometry(MultiLineString,4612));
INSERT INTO shibuya_roads (SELECT id, geom FROM shade);
CREATE TABLE shibuya_shades (id integer REFERENCES shibuya_roads(id), time time, rate float);
COPY shibuya_shades (id, time, rate) FROM '/docker-entrypoint-initdb.d/sun_expo_flatten.csv' DELIMITERS ',' CSV HEADER;
```
