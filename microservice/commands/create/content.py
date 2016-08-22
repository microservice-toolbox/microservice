import os
from jinja2 import Environment, FileSystemLoader
from microservice.core.ui import success, fail, warning, info

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

class Content:
    directory = os.getcwd()

    def __init__(self, name):
        self.name = name
        self.directory = os.path.join(os.getcwd(), self.name)
        env = Environment(loader=FileSystemLoader(self.directory))
        template = env.get_template('README.md')
        result = template.render(project_name='ola')
        with open(os.path.join(self.directory, 'README.md'), 'w+') as myfile:
            myfile.write(result)
