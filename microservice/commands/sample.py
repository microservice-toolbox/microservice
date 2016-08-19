import argparse
import sys
import click


def run(args):
    if args.foo is not None:
        click.echo(args.foo)
        return
    click.echo("I'm a sample command. override me")


def sample():
    parser = argparse.ArgumentParser(description='Sample command (Override Me)')
    parser.add_argument(
            '--foo',
            help='print another default sample message',
    )
    args = parser.parse_args(sys.argv[2:])
    run(args)
