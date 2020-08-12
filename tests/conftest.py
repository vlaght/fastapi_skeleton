from fastapi.testclient import TestClient
from pytest import fixture

from main import app
from models.database import get_engine
from models.database import metadata


@fixture(scope='session')
def client():
    engine = get_engine(target='test')
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

    return TestClient(app)
