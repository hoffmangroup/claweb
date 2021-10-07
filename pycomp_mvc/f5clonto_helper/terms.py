import operator

MERGE_SEPARATOR = ';;'


class TermMerger:
    def __init__(self, terms, merge_separator=MERGE_SEPARATOR):
        self.terms = sorted(terms, key=operator.attrgetter('name'))
        self.term_ids = [term.term_id for term in self.terms]
        self.merge_separator = merge_separator

    def merge(self):

        name = self.merge_separator.join(term.name for term in self.terms)
        term_id = self.merge_separator.join(self.term_ids)

        term = Term(name=name, term_id=term_id,
                    merge_separator=self.merge_separator)

        term.is_a = self.get_new_is_a()
        term.relationship = self.get_new_relationships()

        return term

    def get_new_is_a(self):
        all_is_a = set()
        for term in self.terms:
            all_is_a.update(term.is_a)

        # exclude the is_a referring to merged terms
        new_is_a = all_is_a - frozenset(self.term_ids)
        return list(new_is_a)

    def get_new_relationships(self):
        new_rel = set()
        for term in self.terms:
            for rel in term.relationship:
                rel_type, term_id = rel
                # exclude relationships referring to merged terms
                if term_id not in self.term_ids:
                    new_rel.add(rel)

        return list(new_rel)


class Term(object):
    """
    Stores terms by turning term keys into object attributes.
    """

    def __init__(self, name='', term_id='', rows=[],
                 merge_separator=MERGE_SEPARATOR):

        self.term_id = term_id
        self.name = name
        self.is_a = []
        self.relationship = []
        self.subset = []
        self.merge_separator = merge_separator

        for tag, value in rows:
            if tag == 'is_a':
                self.is_a.append(value.split(' ! ')[0])
            elif tag == 'id':
                self.term_id = value
            elif tag == 'name':
                self.name = value.replace('/', '-')
            elif tag == 'relationship':
                self.relationship.append(tuple(value.split(' ! ')[0].split(' ')[:2]))
            elif tag == 'subset':
                self.subset.append(value)

    @property
    def is_merged_term(self):
        return self.merge_separator in self.term_id

    def update_is_a(self, update_dict):
        new_term_ids = set()
        for term_id in self.is_a:
            new_term_id = update_dict.get(term_id, term_id)
            new_term_ids.add(new_term_id)

        self.is_a = list(new_term_ids)

    def update_relationship(self, update_dict):
        new_relationships = set()
        for rel_type, term_id in self.relationship:
            new_term_id = update_dict.get(term_id, term_id)
            new_relationships.add((rel_type, new_term_id))

        self.relationship = list(new_relationships)

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.term_id}, {self.name})')


class CLTerm(Term):
    """
    Inherits from Term. This object is used to store the cell lineage
    terms from an obo file. It combines term information and
    the list of samples associated to it.
    """

    def __init__(self, term, samples=[], merge_separator=MERGE_SEPARATOR):
        super().__init__(term.name, term.term_id, merge_separator=merge_separator)
        self.is_a = term.is_a
        self.relationship = term.relationship
        self.samples = samples

    @property
    def has_sample(self):
        return self.nb_of_sample > 0

    @property
    def nb_of_sample(self):
        return len(self.samples)

    @property
    def samples_to_str(self):
        return ",".join(self.samples).replace('FF:', '')

    @classmethod
    def from_clterms(cls, terms=[]):
        new_term = TermMerger(terms).merge()

        samples = set()
        for term in terms:
            samples.update(term.samples)

        return cls(new_term, list(samples))

    def samples_in_common(self, term):
        return frozenset(self.samples).intersection(term.samples)

    def has_same_sample_set(self, term):
        return frozenset(self.samples) == frozenset(term.samples)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.term_id}, {self.name})'


