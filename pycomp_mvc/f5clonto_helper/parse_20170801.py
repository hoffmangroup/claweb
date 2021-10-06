#!/usr/bin env python3
import argparse
import sys
from collections import defaultdict
from typing import List, Dict

import yaml

from .terms import CLTerm
from .terms import Term


def is_f5_sample(term_id):
    return term_id.startswith('FF') and '-' in term_id


class Terms:

    def __init__(self, filename):

        self.terms = dict()

        f = open(filename, 'r')

        while 1:
            line = f.readline()
            rows = []

            if not line:
                break

            if "[Term]" not in line.strip():
                continue

            while 1:
                line = f.readline().strip().split(': ')
                if not line[0]:
                    break
                line = [line[0], ": ".join(line[1:])]
                rows.append(line)
            term = Term(rows=rows)
            self.terms[term.term_id] = term

        f.close()

    def ancestors(self, term_id, func, s):
        """
        Return all the ancestors of `term_id` accessible through `is_a` where `func` return True.
        :param term_id: get the ancestors of `term_id`.
        :param func: evaluate the parents with this function.
        :param s: set ancestor's term ids.
        :return: s
        """
        for parent_id in self.terms[term_id].is_a:
            if func(parent_id):
                s.add(parent_id)
                s.update(self.ancestors(parent_id, func, s))
        return s

    def get_cl_human_samples(self, human_sample="FF:0000210", tissue_sample='FF:0000004'):
        cl_human_samples = defaultdict(set)

        f5_sample_term_ids = [term_id
                              for term_id in self.terms
                              if is_f5_sample(term_id)]

        for term_id in f5_sample_term_ids:

            ancestors = self.ancestors(term_id, lambda x: x.startswith('FF:'), set())
            # current also need to be checked
            # because samples can derive from CLs
            ancestors.add(term_id)

            if human_sample not in ancestors:
                continue

            if tissue_sample in ancestors:
                continue

            if 'phase1' not in self.terms[term_id].subset:
                continue

            for ancestor in ancestors:
                if not self.terms[ancestor].relationship:
                    continue
                for rel_type, parent in self.terms[ancestor].relationship:
                    if rel_type == 'derives_from' and parent.startswith('CL:'):
                        cl_human_samples[parent].add(term_id)
                        parent_ancestors = self.ancestors(parent, lambda x: x.startswith('CL:'), set())
                        for parent_ancestor in parent_ancestors:
                            cl_human_samples[parent_ancestor].add(term_id)

        # convert set of samples to list of samples
        d = {k: list(v) for k, v in cl_human_samples.items()}
        return d

    def cl_terms(self):
        term_id_to_cl_term = dict()
        cl_human_samples = self.get_cl_human_samples()

        for term_id, term in self.terms.items():
            if not term_id.startswith("CL:"):
                continue

            if term_id not in cl_human_samples:
                term_id_to_cl_term[term_id] = CLTerm(term, [])
            else:
                term_id_to_cl_term[term_id] = CLTerm(term, cl_human_samples[term_id])

        return term_id_to_cl_term

    def get_terms_with_same_samples(self) -> List[List[CLTerm]]:
        """Return a list that lists the terms with the exact same non-empty set of samples.

        :return: List[List[CLTerm]]
        """
        res: List[List[CLTerm]] = []

        # keep track of the terms known with same
        # sample set as another term to avoid
        # reporting a term twice.
        processed_terms = set()

        # exclude terms without samples to avoid considering them as similar.
        terms_with_samples = [term
                              for term in self.cl_terms().values()
                              if term.has_sample]

        # for each term, check every following term
        for i, term in enumerate(terms_with_samples[:-1]):
            # skip term if we already know that it is similar to another term.
            if term in processed_terms:
                continue

            # check if the following samples have the same samples
            similar_terms = [comp_term
                             for comp_term in terms_with_samples[i+1:]
                             if set(comp_term.samples) == set(term.samples)]

            # add current term to list of similar samples
            # and update `res`
            if similar_terms:
                similar_terms.append(term)
                processed_terms.update(similar_terms)
                res.append(similar_terms)

        return res

    def get_oldest_parent(self, term_ids):
        for i, term_id in enumerate(term_ids):
            ancestors = self.ancestors(term_id, lambda x: x.startswith('CL:'), set())
            has_term_in_ancestors = any(_id in ancestors for _id in term_ids)
            if not has_term_in_ancestors:
                return i, term_id

    def get_deepest_child_from_term_ids(self, term_ids: List[str]) -> str:
        """Deepest child is a synonym for most specialized cell type.
        Return the term_id of the cell type that has the most term_id from terms_ids in it's ancestors.
        example: A - B - C - D
                       \
                         E
        D has 3 ancestors, E has 2 ancestors. D is the deepest child of A.

        :param term_ids: list of strings containing term_ids (["CL:...", "CL:..."], ...)
        """
        deepest_id = term_ids[0]
        deepest_score = 0
        for term_id in term_ids:
            ancestors = self.ancestors(term_id, lambda x: x.startswith('CL:'), set())
            score = sum(1 for _id in term_ids if _id in ancestors)
            if score > deepest_score:
                deepest_score = score
                deepest_id = term_id

        return deepest_id

    def collapse_cl_terms(self):
        """ Collapse CL terms with the same set of non-empty sample.
        Update the source and the target of the edges that refer to a
        collapsed CL term.

        XXX: use https://github.com/dhimmel/obonet
        to manipulate the cell ontology.
        Or, store nodes and edges separately.

        :return: Dict[str, CLTerm]
        """

        res: Dict[str, CLTerm] = self.cl_terms()
        cl_to_new_term = dict()
        list_of_similar_terms = self.get_terms_with_same_samples()

        # merge similar terms
        for similar_terms in list_of_similar_terms:
            # merge terms
            merged_term = CLTerm.merge_terms(similar_terms)

            # index new term and delete the old ones
            res[merged_term.term_id] = merged_term
            for term in similar_terms:
                cl_to_new_term[term.term_id] = merged_term
                del res[term.term_id]

        # update the is_a and relationships of all terms
        for term_id, term in res.items():
            # update is_a
            new_is_a = set()
            for is_a in term.is_a:
                if is_a in cl_to_new_term:
                    new_is_a.add(cl_to_new_term[is_a].term_id)
                else:
                    new_is_a.add(is_a)
            term.is_a = list(new_is_a)

            # update relationship
            new_relationship = set()
            for rel_type, parent in term.relationship:
                if parent in cl_to_new_term:
                    new_relationship.add((rel_type, cl_to_new_term[parent].term_id))
                else:
                    new_relationship.add((rel_type, parent))
            term.relationship = list(new_relationship)

        return res


def main(input_cl_ontology, output_group_and_comparison):
    main_terms = Terms(input_cl_ontology)
    terms = main_terms.collapse_cl_terms().values()
    terms = [term for term in terms if len(term.samples) > 10]

    nodes_print_id = {}
    nodes_print_name = {}
    for term in terms:
        if ";;" in term.term_id:
            youngest_child = main_terms.get_deepest_child_from_term_ids(term.term_id.split(";;"))
            nodes_print_id[term.name] = youngest_child
            nodes_print_name[term.name] = main_terms.cl_terms()[youngest_child].name

    yaml_dict = dict()
    group_definitions = [
        {
            'id': term.term_id,
            'name': term.name,
            'print_name': nodes_print_name.get(term.name, term.name),
            'print_id': nodes_print_id.get(term.name, term.term_id),
            'samples': sorted([sample.replace('FF:', '') for sample in term.samples])
        } for term in terms]

    comparisons = []
    for i, term0 in enumerate(terms):
        for term1 in terms[i + 1:]:
            if not set.intersection(set(term0.samples), set(term1.samples)):
                comparisons.append({'group1': term0.term_id, 'group2': term1.term_id})

    for i, comparison in enumerate(comparisons):
        comparison['id'] = i

    yaml_dict['group_definitions'] = group_definitions
    yaml_dict['comparisons'] = comparisons

    with open(output_group_and_comparison, 'w') as yaml_file:
        yaml_file.write(yaml.dump(yaml_dict, default_flow_style=False))


def parse_args():
    parser = argparse.ArgumentParser(description='Make group and comparison file from the FANTOM5 cell ontology ')
    parser.add_argument('input_fantom5_ontology', type=str,
                        help='full path to the FANTOM5 cell ontology', )
    parser.add_argument('output_gac_file', type=str, help='output filepath')
    args = parser.parse_args(sys.argv[1:])
    return args


def cli_make_gac():
    args = parse_args()
    main(args.input_fantom5_ontology, args.output_gac_file)


if __name__ == '__main__':
    cli_make_gac()
