import shutil
import os
from microservice.core.ui import success, fail, warning, info, Colors

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

class Directory:
    template = "/home/herve/.dev/python/microservice/toolbox/project-builder"
    source = os.path.join(template, 'packaging')
    available_templates_path = os.path.join(template, 'templates')
    available_options_path = os.path.join(template, 'optionals')
    available_templates = []
    available_options = []
    user_choice = ""
    dest = os.getcwd()

    def __init__(self, name):
        self.name = name
        self.dest = os.path.join(os.getcwd(), self.name)
        self.initialize()

    def initialize(self):
        try:
            print("Setup base project packaging...", end=' ')
            self.setup_base_project()
            success('OK !')
        except:
            fail('Failed !')
            warning('Directory already exist')
            exit(1)
        try:
            print("Loading all available templates...", end=' ')
            self.discover_available_templates()
            success('OK !')
        except:
            fail('Failed !')
            exit(1)

        self.choose_type()
        success("Selected template: {0}".format(self.user_choice))
        self.setup_template()
        success("Project template installed !")

        try:
            print("Loading all available options...", end=' ')
            self.discover_optionnal_configuration()
            success('OK !')
        except:
            fail('Loading templates failed !')
            exit(1)

        self.choose_options()
        success("Done !")

    def setup_base_project(self):
        base = self.source
        shutil.copytree(base, self.dest)

    def setup_template(self):
        base = os.path.join(self.available_templates_path,
            self.user_choice, 'sources')

        if not os.path.isdir(base):
            fail("Source directory doesn't exist !")

        to = os.path.join(self.dest, 'sources')
        print("setup sources...", end=" ")
        self.setup_sources(base, to)
        success('OK !')
        to = os.path.join(self.dest)
        base = os.path.join(self.available_templates_path,
            self.user_choice, 'packaging')
        print("override base packaging...", end=" ")
        self.override_packaging(base, to)
        success('OK !')

    def setup_sources(self, base, to):
        self.setup_dir(base, to, 'sources')

    def override_packaging(self, base, to):
        self.setup_dir(base, to, 'packaging')

    def setup_dir(self, base, to, root):
        for dirname, dirnames, filenames in os.walk(base):
            current = None
            for mydir in dirnames:
                shutil.copytree(
                    os.path.join(dirname, mydir), os.path.join(to, mydir))

            for myfile in filenames:
                if os.path.basename(dirname) == root:
                    if ".microservice.yaml" != myfile:
                        shutil.copy(os.path.join(dirname, myfile), to)


    def discover_available_templates(self):
        find = False
        for dirname, dirnames, filenames in os.walk(
            self.available_templates_path):
            if not find:
                self.available_templates = dirnames
                return

    def discover_optionnal_configuration(self):
        find = False
        for dirname, dirnames, filenames in os.walk(
            self.available_options_path):
            if not find:
                self.available_options = dirnames
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
        self.user_choice = self.available_templates[int(choice) - 1]

    def choose_options(self):
        for option in self.available_options:
            choice = input('{1}Use this option {0} [n/y] ?{2} '.format(
                option,
                Colors.WARNING, Colors.ENDC))
            if choice != 'y':
                continue
            try:
                print("Installing {0}...".format(option), end='')
                to = os.path.join(self.dest)
                base = os.path.join(self.available_options_path, option)
                self.setup_dir(base, to, option)
                success("OK !")
            except:
                fail("Failed !")
