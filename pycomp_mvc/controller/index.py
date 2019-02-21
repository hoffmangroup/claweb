import os
import yaml
from jinja2 import Environment, FileSystemLoader


def main(config_file):

    template_folder = os.path.join(os.path.dirname(__file__), '..', 'view')
    env = Environment(loader = FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'index.tpl'

    output = template.render(site=config_file['website'], tpl=child_template)
    with open(os.path.join(config_file['website']['output'], "index.html"), "wb") as f:
        f.write(output.encode( "utf-8" ))

    print('index.html generated')
