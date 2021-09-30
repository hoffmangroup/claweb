import operator


class Term(object):
    """
    Stores terms by turning term keys into object attributes.
    """

    def __init__(self, name='', term_id=0, rows=[]):

        self.term_id = term_id
        self.name = name
        self.is_a = []
        self.relationship = []
        self.subset = []

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

    @staticmethod
    def merge_terms(terms=[]):
        terms.sort(key=operator.attrgetter('name'))
        new_term = Term(name=';;'.join([term.name for term in terms]))
        new_term.term_id = ';;'.join([term.term_id for term in terms])
        terms_id = [term.term_id for term in terms]

        for term in terms:
            new_term.is_a.extend([is_a for is_a in term.is_a if is_a not in terms_id])
            new_term.relationship.extend(
                [relationship for relationship in term.relationship if relationship[1] not in terms_id])

        new_term.is_a = list(set(new_term.is_a))
        new_term.relationship = list(set(new_term.relationship))

        return new_term

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.term_id}, {self.name})')


class CLTerm(Term):
    """
    Inherits from Term. This object is used to store the cell lineage
    terms from an obo file. It combines term information and
    the list of samples associated to it.
    """

    def __init__(self, term, samples=[]):
        super().__init__()
        self.term_id = term.term_id
        self.name = term.name
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

    @staticmethod
    def merge_terms(terms=[]):
        new_term = Term.merge_terms(terms)

        samples = []
        for term in terms:
            samples.extend(term.samples)

        return CLTerm(new_term, list(set(samples)))

    def samples_in_common(self, term):
        samples0 = set(self.samples)
        samples1 = set(term.samples)

        return set.intersection(samples0, samples1)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.term_id}, {self.name})'

