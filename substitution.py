class SubstitutionException(Exception):
    def __init__(self, text):
        self.txt = text


class Substitution:
    def __init(self, const, pattern):
        self.const = const
        self.pattern = pattern
        self.t_dict = dict()

    def algorithm(self, i_c, i_p):

        if self.pattern[i_p].type == 'e':
            if i_c == len(self.const) - 1:
                return True
            return self.e(i_c, i_p)

        elif self.pattern[i_p].type == 'v':
            if i_c == len(self.const) - 1:
                return False
            return self.v(i_c, i_p)

        elif self.pattern[i_p].type == 't':
            if i_c == len(self.const) - 1:
                return False
            return self.t(i_c, i_p)

        elif self.pattern[i_p].type == 's':
            if i_c == len(self.const) - 1:
                return False
            return self.s(i_c, i_p)

        raise SubstitutionException('Unknown atom type')

    def e(self, i_c, i_p):
        for i in range(len(self.const) - i_c - 1, -1, -1):
            if self.algorithm(i_c + i, i_p + 1):
                return True
        return False

    def v(self, i_c, i_p):
        for i in range(len(self.const) - i_c - 1, 0, -1):
            if self.algorithm(i_c + i, i_p + 1):
                return True
        return False

    def t(self, i_c, i_p):
        if self.pattern[i_p].val in self.t_dict:
            if self.const[i_c] != self.t_dict[self.pattern[i_p].val]:
                return False
        else:
            self.t_dict[self.pattern[i_p].val] = self.const[i_c]
            return self.algorithm(i_c + 1, i_p + 1)

    def s(self, i_c, i_p):
        if self.const[i_c] == self.pattern[i_p].val:
            return self.algorithm(i_c + 1, i_p + 1)
        return False
