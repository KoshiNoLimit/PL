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
        elif val.startswith('s.'):
            return 's'
        else:
            return 'c'

    def __repr__(self):
        return self.val  # +'|'+self.val

    def __eq__(self, other):
        return self.val == other.val

    def __hash__(self):
        return hash(self.val)


class SubAtom:

    def __init__(self, val, power):
        self.val = val
        self.len = power[0]
        self.have_plus = power[1]

    def __repr__(self):
        return self.val + ':' + str(self.len) + '+' if self.have_plus else ''

    def __eq__(self, other):
        return \
            self.val == other.val and \
            self.len == other.len and \
            self.have_plus == other.have_plus

    def __hash__(self):
        return hash(str(self.val)+str(self.len)+str(self.have_plus))


def atomize_sample(sample):
    vals = sample.split(' ')
    return [Atom(val) for val in vals]
