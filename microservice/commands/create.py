import argparse
import sys
import shutil
import os
from microservice.core.ui import success, fail, warning, info

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

class ProjectBuilder:
    template = "/home/herve/.dev/python/microservice/toolbox/project-builder"
    source = os.path.join(template, 'packaging')
    available_templates_path = os.path.join(template, 'templates')
    available_templates = []

    def __init__(self, name):
        self.name = name
        self.initialize()
        self.choose_type()

    def initialize(self):
        try:
            print("Setup base project packaging...")
            self.setup_base_project()
            success('Setup OK')
        except:
            fail('Setup base failed !')
        try:
            print("Loading all available templates...")
            self.discover_available_templates()
            success('Loading OK')
        except:
            fail('Loading templates failed !')

    def setup_base_project(self):
        dest = os.path.join(os.getcwd(), self.name)
        base = self.source
        shutil.copytree(base, dest)

    def discover_available_templates(self):
        find = False
        for dirname, dirnames, filenames in os.walk(self.available_templates_path):
            if not find:
                self.available_templates = dirnames
                return

    def choose_type(self):
        for index, template in enumerate(self.available_templates):
            print("{0}. {1}".format(index, template))
        choice = input("Choose your template : ")

def run(args):
    builder = ProjectBuilder(args.to)


def create():
    parser = argparse.ArgumentParser(
        description='Create a new microservice application')
    parser.add_argument('from', help='Template to use')
    parser.add_argument('to', help='New project name')
    args = parser.parse_args(sys.argv[2:])
    run(args)
