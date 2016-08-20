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
    user_choice = ""
    dest = os.getcwd()

    def __init__(self, name):
        self.name = name
        self.dest = os.path.join(os.getcwd(), self.name)
        self.initialize()

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

        self.choose_type()
        success("Selected template: {0}".format(self.user_choice))
        self.setup_template()

    def setup_base_project(self):
        base = self.source
        shutil.copytree(base, self.dest)

    def setup_template(self):
        base = os.path.join(self.available_templates_path,
            self.user_choice, 'sources')

        if not os.path.isdir(base):
            fail("Source directory doesn't exist !")

        to = os.path.join(self.dest, 'sources')
        self.setup_sources(base, to)

    def setup_sources(self, base, to):
        for dirname, dirnames, filenames in os.walk(base):
            current = None
            for mydir in dirnames:
                print(os.path.join(dirname, mydir))
                shutil.copytree(os.path.join(dirname, mydir), os.path.join(to, mydir))

            for myfile in filenames:
                if os.path.basename(dirname) == 'sources':
                    shutil.copy(os.path.join(dirname, myfile), to)

    def discover_available_templates(self):
        find = False
        for dirname, dirnames, filenames in os.walk(
            self.available_templates_path):
            if not find:
                self.available_templates = dirnames
                return

    def list_templates(self):
        for index, template in enumerate(self.available_templates):
            print("{0}. {1}".format(index + 1, template))

    def is_valid_choice(self, choice):
        try:
            choice = int(choice)
        except ValueError:
            return False

        if choice <= 0 or choice > len(self.available_templates) :
            return False
        return True

    def choose_type(self):
        choice = 0
        self.list_templates()
        while not self.is_valid_choice(choice):
            choice = input("Choose your template : ")
        self.user_choice = self.available_templates[int(choice)]

def run(args):
    builder = ProjectBuilder(args.to)


def create():
    parser = argparse.ArgumentParser(
        description='Create a new microservice application')
    parser.add_argument('from', help='Template to use')
    parser.add_argument('to', help='New project name')
    args = parser.parse_args(sys.argv[2:])
    run(args)
