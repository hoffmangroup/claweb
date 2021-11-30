"""
Created on Oct 7, 2013

@author: mmendez
"""

import os

from jinja2 import Environment, FileSystemLoader
from ...model import comparisons as comparison_model


def comparisons(cfg, group_and_comparisons, comp_id):
    template_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'view')
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')

    site = cfg['website'].copy()
    if site['url'] == '.':
        site['url'] = '..'

    if not os.path.exists(os.path.join(cfg['website']['output'], "comparisons")):
        os.makedirs(os.path.join(cfg['website']['output'], "comparisons"))

    dataset_genes, g1_name, g2_name = comparison_model.comparison(cfg, group_and_comparisons, comp_id)

    # check if there is results for this comparison and choose the right template
    if sum([dataset['n_genes'] for dataset in dataset_genes]):
        child_template = 'comparisons.tpl'
    else:
        child_template = 'comparison_empty.tpl'

    output = template.render(dataset_genes=dataset_genes, group1_name=g1_name, group2_name=g2_name,
                             site=site, tpl=child_template)

    page_path = os.path.join(cfg['website']['output'], 'comparisons', str(comp_id) + ".html")
    print(page_path, "generated")
    with open(page_path, "wb") as f:
        f.write(output.encode("utf-8"))
