import argparse
import sys
from microservice.commands.create.directory import Directory
from microservice.commands.create.content import Content


def create():
    parser = argparse.ArgumentParser(
    description='Create a new microservice application')
    parser.add_argument('from', help='Template to use')
    parser.add_argument('to', help='New project name')
    args = parser.parse_args(sys.argv[2:])
    Directory(args.to)
    Content(args.to)
