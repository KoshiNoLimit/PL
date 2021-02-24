from algorithm.atom import Atom
from collections import Counter
import algorithm.pattern_format as pf
from copy import deepcopy
import logging


class SubstitutionException(Exception):
    def __init__(self, text):
        self.txt = text


class ConstSubstitution:
    """Подстановка константного выражения в P"""
    def __init__(self, const, pattern):
        # print('P&C', pattern, const)
        self.const = const
        self.pattern = pattern
        self.val_dict = dict()

    def algorithm(self, i_c=0, i_p=0):
        if i_p == len(self.pattern):
            if i_c == len(self.const):
                return True
            else:
                return False

        if self.pattern[i_p].type == 'e':
            if i_c == len(self.const):
                for i in range(i_p+1, len(self.pattern)):
                    if self.pattern[i].type != 'e':
                        return False
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

        elif self.pattern[i_p].type == 'c':
            if i_c == len(self.const):
                return False
            return self.c(i_c, i_p)

        elif self.pattern[i_p].type == 's':
            if i_c == len(self.const):
                return False
            return self.s(i_c, i_p)

        else:
            raise SubstitutionException('Unknown atom type: ' + self.pattern[i_p].type)

    def e(self, i_c, i_p):
        for i in range(len(self.const) - i_c, -1, -1):
            temp_d = deepcopy(self.val_dict)
            if self.algorithm(i_c + i, i_p + 1):
                return True
            self.val_dict = deepcopy(temp_d)
        return False

    def v(self, i_c, i_p):
        for i in range(len(self.const) - i_c, 0, -1):
            if self.algorithm(i_c + i, i_p + 1):
                return True
        return False

    def t(self, i_c, i_p):
        if self.pattern[i_p].val in self.val_dict:
            if self.const[i_c] != self.val_dict[self.pattern[i_p].val]:
                return False
            else:
                return self.algorithm(i_c + 1, i_p + 1)
        else:
            self.val_dict[self.pattern[i_p].val] = self.const[i_c]
            return self.algorithm(i_c + 1, i_p + 1)

    def c(self, i_c, i_p):
        if self.const[i_c] == self.pattern[i_p].val:
            return self.algorithm(i_c + 1, i_p + 1)
        return False

    def s(self, i_c, i_p):
        if self.pattern[i_p].val in self.val_dict:
            if self.const[i_c] != self.val_dict[self.pattern[i_p].val]:
                return False
            else:
                return self.algorithm(i_c + 1, i_p + 1)
        else:
            if not (self.const[i_c].startswith('A.') or self.const[i_c].startswith('B.')):
                self.val_dict[self.pattern[i_p].val] = self.const[i_c]
                return self.algorithm(i_c + 1, i_p + 1)
            return False


class PToPSubstitution:
    """Подстановка P в P"""
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.val_dict = dict()

    def algorithm(self, i_p1=0, i_p2=0):
        if i_p1 == len(self.p1):
            if i_p2 == len(self.p2):
                return True
            else:
                return False

        if self.p1[i_p1].type == 'e':
            if i_p2 == len(self.p2):
                if self.p1[i_p1].val not in self.val_dict or len(self.val_dict[self.p1[i_p1].val]) == 0:
                    return self.algorithm(i_p1+1, i_p2)
                return False
            return self.e(i_p1, i_p2)

        elif self.p1[i_p1].type == 'c':
            if i_p2 == len(self.p2):
                return False
            return self.c(i_p1, i_p2)

        elif self.p1[i_p1].type == 's':
            if i_p2 == len(self.p2):
                return False
            return self.s(i_p1, i_p2)

        raise SubstitutionException('Unknown atom type: ' + self.p1[i_p1].type)

    def e(self, i_p1, i_p2):
        if self.p1[i_p1].val in self.val_dict:
            for atom in self.val_dict[self.p1[i_p1].val]:
                if atom != self.p2[i_p2]:
                    return False
            return self.algorithm(i_p1 + 1, i_p2 + len(self.val_dict[self.p1[i_p1].val]))

        else:
            for i in range(len(self.p2) - i_p2, -1, -1):
                self.val_dict[self.p1[i_p1].val] = self.p2[i_p2: i_p2 + i]
                dict_copy = self.val_dict.copy()
                if self.algorithm(i_p1 + 1, i_p2 + i):
                    return True
                self.val_dict = dict_copy
            return False

    def c(self, i_p1, i_p2):
        if self.p2[i_p2].val == self.p1[i_p1].val:
            return self.algorithm(i_p1 + 1, i_p2 + 1)
        return False

    def s(self, i_p1, i_p2):
        if self.p1[i_p1].val in self.val_dict:
            if self.val_dict[self.p1[i_p1].val] != self.p2[i_p2]:
                return False
            return self.algorithm(i_p1 + 1, i_p2 + 1)

        else:
            if self.p2[i_p2].type in ['c', 's']:
                self.val_dict[self.p1[i_p1].val] = self.p2[i_p2]
                return self.algorithm(i_p1 + 1, i_p2 + 1)
            return False


def get_Q(p, N):
    """Создание подстановки"""
    q = []
    for atom in p:

        if atom.type == 'e' or atom.type == 'v':
            for i in range(N + 1):
                q.append('A.' + atom.val[2:] + str(i))

        elif atom.type == 't':
            q.append('B.' + atom.val[2:])

        elif atom.type == 's':
            q.append('C.' + atom.val[2:])

        elif atom.type == 'c':
            q.append(atom.val)

        else:
            raise SubstitutionException('Unknown type: ' + atom.type)

    return q


class SplitSubstitution:
    """Все возможные подстановки под повторяющиеся переменные"""
    def __init__(self, p1, p2, EPL_method):
        self.p1 = p1
        self.p2 = p2
        self.EPL_method = EPL_method
        self.splited_vals = set()
        val_free = set()
        val_busy = set()

        for atom in p1:
            if atom.type in ('t', 's'):
                if atom.val in val_busy:
                    self.splited_vals.add(atom)
                else:
                    val_free.add(atom.val)
            elif atom.type == 'e':
                val_busy.update(val_free)

    def algorithm(self):
        p_1 = self.change_p1()
        if not self.EPL_method(p_1, self.p2):
            logging.debug('–––––EPL: ' + str(p_1))
            return []

        count_index_values = [[] for _ in range(len(self.p2))]
        repeated_vals = list(filter(lambda x: x[0] in self.splited_vals, Counter(self.p1).items()))

        for item in Counter(self.p2).items():
            count_index_values[item[1]].append(item[0])

        logging.debug('civ' + str(count_index_values))

        qs = self.get_qs(repeated_vals=repeated_vals, count_index_values=count_index_values)
        repeated_vals = [val[0] for val in repeated_vals]
        qs = list(map(lambda q: dict(zip(repeated_vals, q)), qs))

        subs = []
        for q in qs:
            p_1 = self.p1.copy()
            for i in range(len(p_1)):
                p_1[i] = q.get(p_1[i], p_1[i])
            subs.append(p_1)

        return subs

    def change_p1(self):
        e_index = 0

        for i in range(len(self.p1)):
            if self.p1[i].type == 'e':
                self.p1[i].val = 'e.' + str(e_index)
                e_index += 1

        p_1 = []
        for atom in self.p1:
            if atom in self.splited_vals:
                p_1.append(Atom('e.' + str(e_index)))
                e_index += 1
                p_1.append(atom)
                p_1.append(Atom('e.' + str(e_index)))
                e_index += 1
            else:
                p_1.append(atom)

        pf.t_float_combine(p_1)
        p_1 = list(filter(lambda x: x.type != 'tf', p_1))
        p__1, e_index = [], 0
        for atom in p_1:
            if atom.type == 'e':
                if len(p__1) and p__1[-1].type == 'e':
                    continue
                atom.val = 'e.' + str(e_index)
                e_index += 1
            p__1.append(atom)
        return p__1

    def get_qs(self, i_val=0, busy=None, repeated_vals=None, count_index_values=None):
        if busy is None:
            busy = set()
        qs = []
        atom, cnt = repeated_vals[i_val][0], repeated_vals[i_val][1]

        for ls in count_index_values[cnt:]:
            for val in ls:
                if (val.type == 't' and atom.type != 't') or val in busy:
                    continue

                if i_val < len(repeated_vals) - 1:
                    map(lambda q: qs.append([val] + q),
                        self.get_qs(i_val + 1, set(val) | busy, repeated_vals, count_index_values))
                else:
                    qs.append([val])
        return qs


class TruncatedMap:
    """Усеченное сопоставление с образцом"""
    def __init__(self, n):
        self.e_cnt = n

    def algorithm(self, p1, p2, i_p1=0, i_p2=0, es=None):
        if es is None:
            es = tuple([] for _ in range(self.e_cnt))
        subs = set()

        if len(p1) - i_p1 == 1 and p1[i_p1].type == 'e':
            return {tuple(map(lambda l: tuple(l), es)), }

        if i_p1 == len(p1):
            for i in range(i_p2, len(p2)):
                if p2[i_p2].type != 'e':
                    return {}
            return {tuple(map(lambda l: tuple(l), es)), }

        if i_p2 == len(p2):
            for i in range(i_p2, len(p2)):
                if p2[i_p2].type != 'e':
                    return {}
            return {tuple(map(lambda l: tuple(l), es)), }

        if p2[i_p2].type == 'e':
            if p1[i_p1].type == 'e':
                subs.update(self.step_1(p1, p2, i_p1, i_p2, deepcopy(es)))
                subs.update(self.step_2(p1, p2, i_p1, i_p2, deepcopy(es)))
                subs.update(self.step_3(p1, p2, i_p1, i_p2, deepcopy(es)))
                subs.update(self.step_4(p1, p2, i_p1, i_p2, deepcopy(es)))

            elif p1[i_p1].type == 'tf':
                subs.update(self.step_1(p1, p2, i_p1, i_p2, deepcopy(es)))
                subs.update(self.step_2(p1, p2, i_p1, i_p2, deepcopy(es)))

            elif p1[i_p1].type in ['t', 's', 'c']:
                subs.update(self.step_2(p1, p2, i_p1, i_p2, deepcopy(es)))

            else:
                raise SubstitutionException('Unknown type of val' + p1[i_p1].type)

        elif p2[i_p2].type in ('c', 't', 'tf') and p1[i_p1].type == 'e':
            subs.update(self.step_3(p1, p2, i_p1, i_p2, deepcopy(es)))
            subs.update(self.step_4(p1, p2, i_p1, i_p2, deepcopy(es)))

        elif p2[i_p2].type == 'c' and p1[i_p1].type in ('s', 't', 'tf'):
            subs.update(self.step_5(p1, p2, i_p1, i_p2, deepcopy(es)))

        elif p2[i_p2].type in ('t', 'tf') and p1[i_p1].type in ('t', 'tf'):
            subs.update(self.step_5(p1, p2, i_p1, i_p2, deepcopy(es)))

        elif p2[i_p2] == p1[i_p1]:
            subs.update(self.step_6(p1, p2, i_p1, i_p2, deepcopy(es)))

        else:
            return {}

        return subs

    def step_1(self, p1, p2, i_p1, i_p2, es):
        es[int(p2[i_p2].val[2:])].append(p1[i_p1])
        return self.algorithm(p1, p2, i_p1 + 1, i_p2, es)

    def step_2(self, p1, p2, i_p1, i_p2, es):
        return self.algorithm(p1, p2, i_p1, i_p2 + 1, es)

    def step_3(self, p1, p2, i_p1, i_p2, es):
        return self.algorithm(p1, p2, i_p1 + 1, i_p2, es)

    def step_4(self, p1, p2, i_p1, i_p2, es):
        if p2[i_p2].type == 'e':
            es[int(p2[i_p2].val[2:])].append('None')
        return self.algorithm(p1, p2, i_p1, i_p2 + 1, es)

    def step_5(self, p1, p2, i_p1, i_p2, es):
        p_1 = deepcopy(p1)
        for i in range(len(p_1)):
            if p_1[i] == p1[i_p1]:
                p_1[i] = p2[i_p2]
        return self.algorithm(p_1, p2, i_p1 + 1, i_p2 + 1, es)

    def step_6(self, p1, p2, i_p1, i_p2, es):
        return self.algorithm(p1, p2, i_p1 + 1, i_p2 + 1, es)
