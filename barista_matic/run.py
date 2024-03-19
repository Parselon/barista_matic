import sys
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from barista_matic.entrypoints.interactive_cli import InteractiveCli
from barista_matic.service_layer.services import BaristaMatic
from barista_matic.adapters.repository import SQLAlchemyRepository

from barista_matic.adapters.orm import start_mappers, metadata


def get_engine():
    return create_engine(os.getenv("DB"))


def run_interactive_cli():
    engine = get_engine()
    #metadata.create_all(engine)
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
