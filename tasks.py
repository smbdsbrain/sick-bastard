import logging
import pathlib

from invoke import task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
Session = sessionmaker(autocommit=True)


@task(default=True)
def run(ctx):
    """
    Run the app
    """

    from sick_bastard.chain import add_corpus

    ctx.config.engine = engine = create_engine(ctx.config.postgres)
    ctx.config.connection = engine.connect()
    Session.configure(bind=engine)

    work_dir = pathlib.Path(__file__).parent / 'corpuses'
    for file in work_dir.iterdir():
        corpus = file.read_text(encoding='utf-8')
        add_corpus(ctx.config, corpus)


@task
def build_phrase(ctx):
    from sick_bastard.chain import build_phrase

    ctx.config.engine = engine = create_engine(ctx.config.postgres)
    ctx.config.connection = engine.connect()
    Session.configure(bind=engine)

    build_phrase(ctx.config)
