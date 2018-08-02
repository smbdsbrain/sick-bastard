import logging

import asyncio
from invoke import task

logging.basicConfig(level=logging.INFO)


@task(default=True)
def run(ctx):
    """
    Run the app
    """

    from sick_bastard.chain import add_corpus
    with open('corpuses/1') as f:
        corpus = f.read()

    add_corpus(corpus)
