from claweb.extra import load_configs


def get_used_samples(cfg_filepath, gac_filepath):
    cfg, gac = load_configs(cfg_filepath, gac_filepath)

    comparisons = gac["comparisons"]
    cl_ids_in_comparison = []
    for comparison in comparisons:
        cl_ids_in_comparison.append(comparison["group1"])
        cl_ids_in_comparison.append(comparison["group2"])

    groups = gac["group_definitions"]
    groups_in_comparisons = [group
                             for group in groups
                             if group["id"] in cl_ids_in_comparison]

    samples = []
    for group in groups_in_comparisons:
        samples += group["samples"]

    return list(set(samples))




#"../../../PycharmProjects/claweb/test_website/34/global_config.yaml", "../../../PycharmProjects/claweb/test_website/34/20170801_group_and_comparisons.yaml"