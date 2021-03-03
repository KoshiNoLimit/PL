class Atom:
    """Элемент образца"""

    def __init__(self, val):
        self.val = val
        self.type = self._get_type(val)

    @staticmethod
    def _get_type(val):
        if val.startswith('e.'):
            return 'e'
        elif val.startswith('t.'):
            return 't'
        elif val.startswith('s.'):
            return 's'
        else:
            return 'c'

    def __repr__(self):
        return self.val   #+'|'+self.type

    def __eq__(self, other):
        return self.val == other.val

    def __hash__(self):
        return hash(self.val)


class SubAtom:
    """Атом-подстановка"""

    def __init__(self, val, power, generate=False):
        self.val = val
        if generate:
            self.len, self.have_plus = SubAtom._build(power)
        else:
            self.len = power[0]
            self.have_plus = power[1]

    @staticmethod
    def _build(atoms):
        e_exist, tf_cnt = False, 0
        for atom in atoms:
            if atom.type == 'e':
                e_exist = True
            elif atom.type == 'tf':
                tf_cnt += 1
        return tf_cnt, e_exist

    def __repr__(self):
        return self.val + ':' + str(self.len) + ('+' if self.have_plus else '')

    def __eq__(self, other):
        return \
            self.val == other.val and \
            self.len == other.len and \
            self.have_plus == other.have_plus

    def __hash__(self):
        return hash(str(self.val)+str(self.len)+str(self.have_plus))


def atomize_sample(sample):
    if len(sample) == 0:
        return []
    vals = sample.split(' ')
    return [Atom(val) for val in vals]
