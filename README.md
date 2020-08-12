# FastAPI application skeleton [![Build Status](https://travis-ci.com/vlaght/fastapi_skeleton.svg?branch=master)](https://travis-ci.com/vlaght/fastapi_skeleton)
Structured in MVC-like style

### Some of basic requirements
- python 3.8
- asyncpg
- python-psycopg2
- libpq-dev
- python3-dev
- docker
- docker-compose


### Basic, for launch:
```sh
pipenv install
pipenv sync
docker-compose up -d db
uvicorn main:app --reload
```

### For testing:
Set TESTING flag for using test DB instead of main DB
```sh
TESTING=1 pytest
```
