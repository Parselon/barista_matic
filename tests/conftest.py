import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    clear_mappers,
    sessionmaker,
)

from barista_matic.adapters.orm import (
    metadata,
    start_mappers,
)


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite://")
    metadata.create_all(engine)
    start_mappers()
    yield engine
    clear_mappers()


@pytest.fixture
def session(in_memory_db):
    return sessionmaker(in_memory_db)()
