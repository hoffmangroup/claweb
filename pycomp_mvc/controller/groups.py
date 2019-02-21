"""
Created on Oct 7, 2013

@author: mmendez
"""
import json
import pandas as pd
import yaml
import os
from jinja2 import Environment, FileSystemLoader
from ..model import groups as groups_model



def group(config_file, group_and_comparisons, group_id):
    template_folder = os.path.join(os.path.dirname(__file__), '..', 'view')
    env = Environment(loader = FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'group.tpl'

    # if not os.path.exists(os.path.join(cgf['website'][0]['output'], "groups")):
    #     os.makedirs(os.path.join(cgf['website'][0]['output'], "groups"))
    #load the results

    group = groups_model.group(config_file, group_and_comparisons, group_id)
    output = template.render(cl=group, site=config_file['website'], tpl=child_template)

    with open(os.path.join(config_file['website']['output'], "groups", group['id'] + ".html"), "wb") as f:
        f.write(output.encode( "utf-8" ))

    print('group html generated')


def group_list(config_file, group_and_comparisons):
    template_folder = os.path.join(os.path.dirname(__file__), '..', 'view')
    env = Environment(loader = FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'group_list.tpl'

    groups = groups_model.group_list(config_file, group_and_comparisons)
    output = template.render(groups=groups, site=config_file['website'], datasets=config_file['datasets'], tpl=child_template)
    
    with open(os.path.join(config_file['website']['output'], "group_list.html"), "wb") as f:
        f.write(output.encode( "utf-8" ))
    
    print('group_list.html generated')