'''
Created on Oct 7, 2013

@author: mmendez
'''
import os
import yaml
import pandas as pd
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

    
def comparisons(config_file, group_and_comparisons):
    template_folder = os.path.join(os.path.dirname(__file__),'templates')
    env = Environment(loader = FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'comparisons.tpl'

    with open(config_file) as yaml_file:
        cgf = yaml.load(yaml_file)

    with open(group_and_comparisons) as yaml_file:
        group_and_comparisons = yaml.load(yaml_file)

    if not os.path.exists(os.path.join(cgf['website'][0]['output'], "comparisons")):
        os.makedirs(os.path.join(cgf['website'][0]['output'], "comparisons"))

    group_to_name = {group['id']: group['name'] for group in group_and_comparisons['group_definitions']}

    datasets = []

    for dataset in cgf['datasets']:
        df = pd.read_csv(dataset['summary'], sep='\t')
        df = df[(df.robustness == 10) & (df.accuracy > .9)]
        datasets.append(df)

    for comparison in group_and_comparisons['comparisons']:
        dataset_genes = []

        for i, df in enumerate(datasets):
            t = df[df['id'] == int(comparison['id'])].copy()
            t['name1'] = t['cl1'].apply(lambda x: group_to_name[x])
            t['name2'] = t['cl2'].apply(lambda x: group_to_name[x])
            t['short_name'] = t['gene'].apply(lambda x: x.split(':')[-1])
            t['gene_dist_url'] = t['gene'].apply(
                lambda g: os.path.join(cgf['website'][0]['url'], 'gene_distribution', dataset['name'], g))
            t = t[['name1', 'name2','t-test', 'p-value', 'short_name', 'gene_dist_url']]



            rows = [{'name1': row[1],
                     'name2': row[2],
                     'ttest': row[3],
                     'pvalue': row[4],
                     'gene': row[5],
                     'gene_dist_url': row[6]} for row in t.itertuples()]

            if not rows:
                continue

            rows.sort(key=lambda row: abs(row['ttest']), reverse=True)
            dataset_genes.append({'name': cgf['datasets'][i]['name'], 'n_genes': len(rows), 'rows': rows})

        if not sum([dataset['n_genes'] for dataset in dataset_genes]):
            continue

        comparison['group1'] = group_to_name[comparison['group1']]
        comparison['group2'] = group_to_name[comparison['group2']]

        output = template.render(dataset_genes=dataset_genes, comparison=comparison,
                                 site=cgf['website'][0], tpl=child_template)

        with open(os.path.join(cgf['website'][0]['output'], 'comparisons', str(comparison['id']) + ".html"), "wb") as f:
            f.write(output.encode( "utf-8" ))

    print 'comparisons generated'



def comparison_list(config_file, group_and_comparisons):
    template_folder = os.path.join(os.path.dirname(__file__),'templates')
    env = Environment(loader = FileSystemLoader(template_folder))
    template = env.get_template('default.tpl')
    child_template = 'comparison_list.tpl'

    with open(config_file) as yaml_file:
        cgf = yaml.load(yaml_file)

    with open(group_and_comparisons) as yaml_file:
        group_and_comparisons = yaml.load(yaml_file)

    group_to_name = {group['id']: group['name'] for group in group_and_comparisons['group_definitions']}

    group_comparisons = defaultdict(list)

    used_in_comp = lambda group_id, comparison: comparison['group1'] == group_id or comparison['group2'] == group_id

    for group in group_and_comparisons['group_definitions']:
        comparisons = [comp for comp in group_and_comparisons['comparisons'] if used_in_comp(group['id'], comp)]

        if not comparisons:
            continue

        for comparison in comparisons:
            group_comparisons[group['name']].append({
                'url': os.path.join(cgf['website'][0]['url'], 'comparisons', str(comparison['id']) + '.html'),
                'group1': group_to_name[comparison['group1']],
                'group2': group_to_name[comparison['group2']]
            })


    output = template.render(groups=group_comparisons, site=cgf['website'][0], tpl=child_template)

    with open(os.path.join(cgf['website'][0]['output'], "comparison_list.html"), "wb") as f:
        f.write(output.encode( "utf-8" ))


if __name__ == '__main__':
    comparisons('/Users/mickael/Code/pyRRF-sklearn/global_config.yaml', '/Users/mickael/Code/pyRRF-sklearn/group_and_comparisons.yaml')
    # comparison_list('/Users/mickael/Code/pyRRF-sklearn/global_config.yaml', '/Users/mickael/Code/pyRRF-sklearn/group_and_comparisons.yaml')


