__author__ = 'mickael'

from jinja2 import Environment, FileSystemLoader
from ..model import genes as genes_model
from ..model import gene_dist as gene_dist_model
import os


def gene_list(config_file, group_and_comparisons):

    template_folder = os.path.join(os.path.dirname(__file__), '..', 'view')
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'gene_list.tpl'


    datasets_genes, datasets_name = genes_model.gene_list(config_file, group_and_comparisons)

    output = template.render(d=datasets_genes, site=config_file['website'], datasets_name=datasets_name, tpl=child_template)
    with open(os.path.join(config_file['website']['output'], "gene_list.html"), "wb") as f:
        f.write(output.encode("utf-8"))

    print('gene_list generated')


def gene_card(config_file, group_and_comparisons, dataset, gene):

    template_folder = os.path.join(os.path.dirname(__file__), '..', 'view')
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'gene_card.tpl'

    d, gene_dist_url = genes_model.gene_card(config_file, group_and_comparisons, dataset, gene)

    output = template.render(gene=d, site=config_file['website'], gene_dist=gene_dist_url, tpl=child_template)

    with open(os.path.join(config_file['website']['output'], 'genes', dataset['name'], gene + ".html"), "wb") as f:
        f.write(output.encode("utf-8"))

    output = template.render(gene=d, site=config_file['website'], gene_dist=gene_dist_url, tpl=child_template)

    with open(os.path.join(config_file['website']['output'], 'genes', dataset['name'], gene + ".html"), "wb") as f:
        f.write(output.encode("utf-8"))

    print('gene_card generated', gene)


def gene_dist(config_file, group_and_comparisons, dataset, gene):
    template_folder = os.path.join(os.path.dirname(__file__), '..', 'view')
    env = Environment(loader=FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'gene_dist.tpl'

    my_plot = gene_dist_model.gene_dist(config_file, group_and_comparisons, dataset, gene)

    output = template.render(gene=gene, my_plot=my_plot, site=config_file['website'], tpl=child_template)

    with open(os.path.join(config_file['website']['output'], 'gene_distribution', dataset, gene + ".html"), "wb") as f:
        f.write(output.encode("utf-8"))
