from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_database_url
from app.models import Base

engine = None
SessionLocal = None


def init_engine():
    global engine, SessionLocal
    if engine is not None:
        return engine

    engine = create_engine(get_database_url(), echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
    return engine


@contextmanager
def get_session():
    if SessionLocal is None:
        init_engine()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_database():
    init_engine()
    Base.metadata.create_all(engine)
