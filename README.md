# FastAPI application skeleton
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
