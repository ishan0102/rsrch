import click

import download
import push


@click.group()
def cli():
    pass


@cli.command()
def download():
    download.download_papers()


@cli.command()
def push():
    push.push_papers()
