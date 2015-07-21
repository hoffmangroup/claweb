__author__ = 'mickael'


def comparison_list(config_file, group_and_comparisons):

    group_to_name = {group['id']: group['name'] for group in group_and_comparisons['group_definitions']}