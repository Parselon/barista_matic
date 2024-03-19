import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import (
    create_database,
    database_exists,
)

from barista_matic.adapters.orm import start_mappers
from barista_matic.adapters.repository import SQLAlchemyRepository
from barista_matic.entrypoints.interactive_cli import InteractiveCli
from barista_matic.service_layer.services import BaristaMatic

from barista_matic import settings


def get_engine():
    return create_engine(settings.DB)


def run_interactive_cli():
    engine = get_engine()
    start_mappers()
    session = sessionmaker(engine)()
    repository = SQLAlchemyRepository(session)
    barista_matic = BaristaMatic(repository)
    cli = InteractiveCli(barista_matic)
    cli.execute()


def create_db_file_if_not_exists():
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url)


def main():
    run_interactive_cli()


if __name__ == "__main__":
    sys.exit(main())
