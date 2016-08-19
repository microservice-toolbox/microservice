import argparse
import sys
import click
import requests


def load():
    r = requests.get('https://api.github.com/users/microservice-registry/repos')
    if r.status_code >= 300:
        print('Loading results fail ({0}) !\n{1}'.format(r.status_code, r.json()))
    return r.json()


def run(args):
    click.echo(click.style("I'm searching {0}".format(args.name), fg='green'))
    data = load()
    for project in data:
        if project['name'] == args.name:
            click.echo("{0}: {1}".format(project['name'], project['description']))
            return project
    click.echo(click.style("No results found !", fg='red'))
    exit(1)


def search():
    parser = argparse.ArgumentParser(
            description='Search package command'
    )
    parser.add_argument(
            'name',
            help='package name',
    )
    args = parser.parse_args(sys.argv[2:])
    run(args)
