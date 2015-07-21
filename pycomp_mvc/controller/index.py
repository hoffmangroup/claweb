'''
Created on Oct 20, 2013

@author: mmendez
'''
import os
import yaml
from jinja2 import Environment, FileSystemLoader


def main(config_file):

    with open(config_file) as yaml_file:
        cgf = yaml.load(yaml_file)

    template_folder = os.path.join(os.path.dirname(__file__),'templates')
    env = Environment(loader = FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'index.tpl'

    output = template.render(site=cgf['website'][0], tpl=child_template)
    with open(os.path.join(cgf['website'][0]['output'], "index.html"), "wb") as f:
        f.write(output.encode( "utf-8" ))

    print 'index.html generated'


if __name__ == '__main__':
    # main('/home/mickael/Code/PycharmProjects/pyrrf-sklearn/global_config_desktop.yaml')
    main('/Users/mickael/Code/pyRRF-sklearn/global_config.yaml')
