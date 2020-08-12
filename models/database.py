import databases
import os
import sqlalchemy

metadata = sqlalchemy.MetaData()

DATABASE_URLS = {
    'main': "postgresql://root@127.0.0.1:5432/db",
    'test': "postgresql://root@127.0.0.1:5432/db_test",
}


def get_db(target: str = 'main'):
    return databases.Database(DATABASE_URLS[target])


def get_engine(target: str = 'main'):
    return sqlalchemy.create_engine(DATABASE_URLS[target])


database = get_db('test') if os.getenv('TESTING') else get_db()
