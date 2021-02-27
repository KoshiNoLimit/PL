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

    @staticmethod
    def build(p, tword_len):
        """Создание константной подстановки из образца"""
        q = []
        for atom in p:

            if atom.type == 'e' or atom.type == 'v':
                for i in range(tword_len + 1):
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

    def __init__(self, const, pattern):
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
                for i in range(i_p + 1, len(self.pattern)):
                    if self.pattern[i].type != 'e':
                        return False
                return True
            return self._e(i_c, i_p)

        elif self.pattern[i_p].type == 'v':
            if i_c == len(self.const):
                return False
            return self._v(i_c, i_p)

        elif self.pattern[i_p].type == 't':
            if i_c == len(self.const):
                return False
            return self._t(i_c, i_p)

        elif self.pattern[i_p].type == 'c':
            if i_c == len(self.const):
                return False
            return self._c(i_c, i_p)

        elif self.pattern[i_p].type == 's':
            if i_c == len(self.const):
                return False
            return self._s(i_c, i_p)

        else:
            raise SubstitutionException('Unknown atom type: ' + self.pattern[i_p].type)

    def _e(self, i_c, i_p):
        for i in range(len(self.const) - i_c, -1, -1):
            temp_d = deepcopy(self.val_dict)
            if self.algorithm(i_c + i, i_p + 1):
                return True
            self.val_dict = deepcopy(temp_d)
        return False

    def _v(self, i_c, i_p):
        for i in range(len(self.const) - i_c, 0, -1):
            if self.algorithm(i_c + i, i_p + 1):
                return True
        return False

    def _t(self, i_c, i_p):
        if self.pattern[i_p].val in self.val_dict:
            if self.const[i_c] != self.val_dict[self.pattern[i_p].val]:
                return False
            else:
                return self.algorithm(i_c + 1, i_p + 1)
        else:
            self.val_dict[self.pattern[i_p].val] = self.const[i_c]
            return self.algorithm(i_c + 1, i_p + 1)

    def _c(self, i_c, i_p):
        if self.const[i_c] == self.pattern[i_p].val:
            return self.algorithm(i_c + 1, i_p + 1)
        return False

    def _s(self, i_c, i_p):
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
                    return self.algorithm(i_p1 + 1, i_p2)
                return False
            return self._e(i_p1, i_p2)

        elif self.p1[i_p1].type == 'c':
            if i_p2 == len(self.p2):
                return False
            return self._c(i_p1, i_p2)

        elif self.p1[i_p1].type == 's':
            if i_p2 == len(self.p2):
                return False
            return self._s(i_p1, i_p2)

        raise SubstitutionException('Unknown atom type: ' + self.p1[i_p1].type)

    def _e(self, i_p1, i_p2):
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

    def _c(self, i_p1, i_p2):
        if self.p2[i_p2].val == self.p1[i_p1].val:
            return self.algorithm(i_p1 + 1, i_p2 + 1)
        return False

    def _s(self, i_p1, i_p2):
        if self.p1[i_p1].val in self.val_dict:
            if self.val_dict[self.p1[i_p1].val] != self.p2[i_p2]:
                return False
            return self.algorithm(i_p1 + 1, i_p2 + 1)

        else:
            if self.p2[i_p2].type in ['c', 's']:
                self.val_dict[self.p1[i_p1].val] = self.p2[i_p2]
                return self.algorithm(i_p1 + 1, i_p2 + 1)
            return False


class SplitSubstitution:
    """Все возможные подстановки под повторяющиеся переменные"""

    def __init__(self, p1, p2, EPL_method):
        self.p1 = p1
        self.p2 = p2
        self.EPL_method = EPL_method
        self.splited_vals = self._find_splits()
        logging.debug('Splited vals:' + str(self.splited_vals))

    def _find_splits(self):
        val_free = set()
        val_busy = set()
        splited_vals = set()

        for atom in self.p1:
            if atom.type in ('t', 's'):
                if atom.val in val_busy:
                    splited_vals.add(atom)
                else:
                    val_free.add(atom.val)
            elif atom.type == 'e':
                val_busy.update(val_free)
        return splited_vals

    def algorithm(self):
        p_1 = self._change_p1()
        if not self.EPL_method(p_1, self.p2):
            return []

        const_index_cnt = [[] for _ in range(len(self.p2))]  # В [i] положим атомы-константы кратности i
        repeated_vals = list(filter(lambda x: x[0] in self.splited_vals, Counter(self.p1).items()))

        for item in filter(lambda x: x[0].type in ('c', 't'), Counter(self.p2).items()):
            const_index_cnt[item[1]].append(item[0])
        if len(repeated_vals) == 0:
            return [deepcopy(self.p1)]
        consts = self._subs_splited(repeated_vals=repeated_vals, c_i_c=const_index_cnt)
        repeated_vals = [val[0] for val in repeated_vals]  # Отбросили количества повторов
        subs_to_splited_vals = list(map(lambda q: dict(zip(repeated_vals, q)), consts))

        p1_variants = []
        for q in subs_to_splited_vals:
            p_1 = self.p1.copy()
            for i in range(len(p_1)):
                p_1[i] = q.get(p_1[i], p_1[i])
            p1_variants.append(p_1)

        return p1_variants

    def _change_p1(self):
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

    def _subs_splited(self, i_val=0, busy=None, repeated_vals=None, c_i_c=None):
        if busy is None:
            busy = set()
        subs = []
        atom, cnt = repeated_vals[i_val][0], repeated_vals[i_val][1]

        for ls in c_i_c[cnt:]:
            for val in ls:
                if (val.type == 't' and atom.type != 't') or val in busy:
                    continue

                if i_val < len(repeated_vals) - 1:
                    map(lambda q: subs.append([val] + q),
                        self._subs_splited(i_val + 1, set(val) | busy, repeated_vals, c_i_c))
                else:
                    subs.append([val])
        return subs


class TruncatedMap:
    """Усеченное сопоставление с образцом"""

    def __init__(self, n):
        self.e_cnt = n

    def algorithm(self, p1, p2, i_p1=0, i_p2=0, es=None):
        if es is None:
            es = [[] for _ in range(self.e_cnt)]
        subs = set()

        # if len(p1) - i_p1 == 1 and p1[i_p1].type == 'e':
        #     return {tuple(map(lambda l: tuple(l) if l is not None else l, es)), }

        if i_p1 == len(p1):
            for i in range(i_p2, len(p2)):
                if p2[i].type != 'e':
                    return {}
            return {tuple(map(lambda l: tuple(l) if l is not None else l, es)), }

        if i_p2 == len(p2):
            for i in range(i_p1, len(p1)):
                if p1[i].type != 'e':
                    return {}
            return {tuple(map(lambda l: tuple(l) if l is not None else l, es)), }

        if p2[i_p2].type == 'e':
            if p1[i_p1].type == 'e':
                subs.update(self._branch_1(p1, p2, i_p1, i_p2, deepcopy(es)))
                subs.update(self._branch_2(p1, p2, i_p1, i_p2, deepcopy(es)))
                # subs.update(self._branch_3(p1, p2, i_p1, i_p2, deepcopy(es)))
                # subs.update(self._branch_4(p1, p2, i_p1, i_p2, deepcopy(es)))

            elif p1[i_p1].type == 'tf':
                subs.update(self._branch_1(p1, p2, i_p1, i_p2, deepcopy(es)))
                subs.update(self._branch_2(p1, p2, i_p1, i_p2, deepcopy(es)))

            elif p1[i_p1].type in ['t', 's', 'c']:
                subs.update(self._branch_2(p1, p2, i_p1, i_p2, deepcopy(es)))

            else:
                raise SubstitutionException('Unknown type of val' + p1[i_p1].type)

        elif p2[i_p2].type in ('c', 't', 'tf') and p1[i_p1].type == 'e':
            subs.update(self._branch_3(p1, p2, i_p1, i_p2, deepcopy(es)))
            subs.update(self._branch_4(p1, p2, i_p1, i_p2, deepcopy(es)))

        elif p2[i_p2].type == 'c' and p1[i_p1].type in ('s', 't', 'tf'):
            subs.update(self._branch_5(p1, p2, i_p1, i_p2, deepcopy(es)))

        elif p2[i_p2].type in ('t', 'tf') and p1[i_p1].type in ('t', 'tf'):
            subs.update(self._branch_5(p1, p2, i_p1, i_p2, deepcopy(es)))

        elif p2[i_p2] == p1[i_p1]:
            subs.update(self._branch_6(p1, p2, i_p1, i_p2, deepcopy(es)))

        else:
            return {}

        return subs

    def _branch_1(self, p1, p2, i_p1, i_p2, es):
        es[int(p2[i_p2].val[2:])].append(p1[i_p1])
        return self.algorithm(p1, p2, i_p1 + 1, i_p2, es)

    def _branch_2(self, p1, p2, i_p1, i_p2, es):
        return self.algorithm(p1, p2, i_p1, i_p2 + 1, es)

    def _branch_3(self, p1, p2, i_p1, i_p2, es):
        return self.algorithm(p1, p2, i_p1 + 1, i_p2, es)

    def _branch_4(self, p1, p2, i_p1, i_p2, es):
        if p2[i_p2].type == 'e':
            if len(es[int(p2[i_p2].val[2:])]) == 0:
                es[int(p2[i_p2].val[2:])] = None
            else:
                return {}
        return self.algorithm(p1, p2, i_p1, i_p2 + 1, es)

    def _branch_5(self, p1, p2, i_p1, i_p2, es):
        p_1 = deepcopy(p1)
        for i in range(len(p_1)):
            if p_1[i] == p1[i_p1]:
                p_1[i] = p2[i_p2]
        return self.algorithm(p_1, p2, i_p1 + 1, i_p2 + 1, es)

    def _branch_6(self, p1, p2, i_p1, i_p2, es):
        return self.algorithm(p1, p2, i_p1 + 1, i_p2 + 1, es)
