import databases
import sqlalchemy

metadata = sqlalchemy.MetaData()

# DATABASE_URL = "sqlite:///./sql_app.db"

DATABASE_URL = "postgresql://root@localhost:5432/db"
database = databases.Database(DATABASE_URL)


def get_db_engine():
    return sqlalchemy.create_engine(DATABASE_URL)


engine = get_db_engine()

metadata.create_all(engine)
