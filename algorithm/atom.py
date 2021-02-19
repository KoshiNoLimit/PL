class Atom:
    def __init__(self, val):
        self.val = val
        self.type = self.get_type(val)

    @staticmethod
    def get_type(val):
        if val.startswith('e.'):
            return 'e'
        elif val.startswith('t.'):
            return 't'
        else:
            return 'c'

    def __repr__(self):
        return self.type+'|'+self.val

    def __eq__(self, other):
        return self.val == other.val

    def __hash__(self):
        return hash(self.val)


def atomize_sample(sample):
    vals = sample.split(' ')
    return [Atom(val) for val in vals]