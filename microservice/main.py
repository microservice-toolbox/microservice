# -*- coding: utf-8 -*-

__author__ = 'Hervé Beraud'
__email__ = 'herveberaud.pro@gmail.com'
__version__ = '0.1.0'

import argparse
import sys
from microservice.commands.search import search as cmd_search
from microservice.commands.create import create as cmd_create
from microservice.core.ui import fail, splash

class Microservice(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
        description='microservice',
        usage='''microservice <command> [<args>]

The most commonly used git commands are:
    sample     A simple sample command to override
        ''')
        epilogue='''Credits :

author: Hervé Beraud
version: 0.1.0
        '''.format(__version__)
        parser.add_argument('command', help='Sub command to run')
        parser.add_argument('--version',
            help='Print version',
            action='version',
            version='microservice {version}'.format(version=__version__))
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            fail('Unrecognized command')
            parser.print_help()
            exit(1)

        splash()
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()


    def search(self):
        cmd_search()

    def create(self):
        cmd_create()


def main(args=None):
    """Console script for microservice"""
    Microservice()


if __name__ == "__main__":
    main()
