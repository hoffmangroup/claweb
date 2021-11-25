import os
from ..model import summary

from jinja2 import Environment, FileSystemLoader


def main(config_file):

    template_folder = os.path.join(os.path.dirname(__file__), '..', 'view')
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'index.tpl'

    n_cell_types = summary.get_number_of_cell_types_with_results(config_file)

    output = template.render(site=config_file['website'], number_of_cl=n_cell_types, tpl=child_template)
    with open(os.path.join(config_file['website']['output'], "index.html"), "wb") as f:
        f.write(output.encode("utf-8"))

    print('index.html generated')
