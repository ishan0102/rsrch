import click

from rsrch import download_papers, push_papers


@click.group()
def cli():
    pass


@cli.command()
def download():
    download_papers()


@cli.command()
@click.argument("arxiv_urls", nargs=-1)
def push(arxiv_urls):
    push_papers(arxiv_urls)


if __name__ == "__main__":
    cli()
