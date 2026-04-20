import os
import pytest
from sqlalchemy import delete
from app.database import get_session, init_engine, init_database
from app.models import InventoryItem


def pytest_configure():
    os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
    init_engine()
    init_database()


@pytest.fixture(autouse=True)
def clear_db():
    with get_session() as session:
        session.execute(delete(InventoryItem))
        session.commit()
        yield


@pytest.fixture(scope="session")
def app():
    from app import create_app

    application = create_app()
    application.config["TESTING"] = True
    return application


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
