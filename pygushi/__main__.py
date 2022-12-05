import sys

import click

from .version import version
from .poetry import PoetryBot
from .author import AuthorBot

def show_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('.'.join(str(i) for i in version))
    ctx.exit()


@click.command()
@click.option('version', '-v', '--version', help='Show the information of the version.',
              is_flag=True, expose_value=False, is_eager=True, callback=show_version)
@click.option('-a', '--author', help='Search an author.', default='')
@click.option('-p', '--poem', '--poetry', help='Search poetries.', default='')
def main(author, poem):
    if author:
        bot = AuthorBot.search(author)
        if bot:
            click.echo(bot.id)
        else:
            click.echo('No information about this author.')
    if poem:
        bot = PoetryBot.search(poem)
        for i in bot:
            click.echo(i.id)
    sys.exit(0)


if __name__ == '__main__':
    main()
