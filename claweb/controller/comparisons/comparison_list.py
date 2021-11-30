__author__ = 'mickael'

import os
from jinja2 import Environment, FileSystemLoader
from ...model import comparisons


def comparison_list(cfg, group_and_comparisons):
    template_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'view')
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'comparison_list.tpl'

    group_comparisons = comparisons.comparison_list(cfg, group_and_comparisons)
    output = template.render(groups=group_comparisons, site=cfg['website'], tpl=child_template)

    with open(os.path.join(cfg['website']['output'], "comparison_list.html"), "wb") as f:
        f.write(output.encode("utf-8"))
