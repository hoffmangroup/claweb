"""
Created on Oct 7, 2013

@author: mmendez
"""
import os
from jinja2 import Environment, FileSystemLoader
from ..model import groups as groups_model


def group(config_file, group_and_comparisons, group_id):
    template_folder = os.path.join(os.path.dirname(__file__), '..', 'view')
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'group.tpl'

    site = config_file['website'].copy()
    if site['url'] == '.':
        site['url'] = '..'

    # load the results
    group = groups_model.group(config_file, group_and_comparisons, group_id)
    output = template.render(cl=group, site=site, tpl=child_template)

    output_dir = os.path.join(config_file['website']['output'], "groups")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, group['print_id'].replace(":", "_") + ".html"), "wb") as f:
        f.write(output.encode("utf-8"))
    print(os.path.join(output_dir, group['print_id'].replace(":", "_") + ".html"))
    print('group html generated: {}'.format(group['print_name']))


def group_list(config_file, group_and_comparisons):
    template_folder = os.path.join(os.path.dirname(__file__), '..', 'view')
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'group_list.tpl'

    groups = groups_model.group_list(config_file, group_and_comparisons)
    output = template.render(groups=groups, site=config_file['website'], datasets=config_file['datasets'], tpl=child_template)
    
    with open(os.path.join(config_file['website']['output'], "group_list.html"), "wb") as f:
        f.write(output.encode("utf-8"))
    
    print('group_list.html generated')
