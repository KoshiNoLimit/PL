class SubstitutionException(Exception):
    def __init__(self, text):
        self.txt = text


class Substitution:
    def __init__(self, const, pattern):
        # print('P&C', pattern, const)
        self.const = const
        self.pattern = pattern
        self.t_dict = dict()

    def algorithm(self, i_c=0, i_p=0):
        """Алгоритм сопосавления образца с константным выражением"""
        if i_p == len(self.pattern):
            if i_c == len(self.const):
                return True
            else:
                return False

        if self.pattern[i_p].type == 'e':
            if i_c == len(self.const):
                return True
            return self.e(i_c, i_p)

        elif self.pattern[i_p].type == 'v':
            if i_c == len(self.const):
                return False
            return self.v(i_c, i_p)

        elif self.pattern[i_p].type == 't':
            if i_c == len(self.const):
                return False
            return self.t(i_c, i_p)

        elif self.pattern[i_p].type == 's':
            if i_c == len(self.const):
                return False
            return self.s(i_c, i_p)

        raise SubstitutionException('Unknown atom type: ' + self.pattern[i_p].type)

    def e(self, i_c, i_p):
        for i in range(len(self.const) - i_c, -1, -1):
            if self.algorithm(i_c + i, i_p + 1):
                return True
        return False

    def v(self, i_c, i_p):
        for i in range(len(self.const) - i_c, 0, -1):
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


class PToPSubstitution:
    """Подстановка P в P"""
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.e_dict = dict()

    def algorithm(self, i_p1=0, i_p2=0):
        if i_p1 == len(self.p1):
            if i_p2 == len(self.p2):
                return True
            else:
                return False

        if self.p1[i_p1].type == 'e':
            if i_p2 == len(self.p2):
                if self.p1[i_p1].val not in self.e_dict or len(self.e_dict[self.p1[i_p1].val]) == 0:
                    return self.algorithm(i_p1+1, i_p2)
                return False
            return self.e(i_p1, i_p2)

        elif self.p1[i_p1].type == 's':
            if i_p2 == len(self.p2):
                return False
            return self.s(i_p1, i_p2)

        raise SubstitutionException('Unknown atom type: ' + self.p1[i_p1].type)

    def e(self, i_p1, i_p2):
        if self.p1[i_p1].val in self.e_dict:
            for atom in self.e_dict[self.p1[i_p1].val]:
                if atom != self.p2[i_p2]:
                    return False
            return self.algorithm(i_p1 + 1, i_p2 + len(self.e_dict[self.p1[i_p1].val]))

        else:
            for i in range(len(self.p2) - i_p2, -1, -1):
                self.e_dict[self.p1[i_p1].val] = self.p2[i_p2: i_p2+i]
                dict_copy = self.e_dict.copy()
                if self.algorithm(i_p1 + 1, i_p2 + i):
                    return True
                self.e_dict = dict_copy
            return False

    def s(self, i_p1, i_p2):
        if self.p2[i_p2].val == self.p1[i_p1].val:
            return self.algorithm(i_p1 + 1, i_p2 + 1)
        return False
