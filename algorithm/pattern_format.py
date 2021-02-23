from collections import Counter
from algorithm.atom import *


class PatternException(Exception):
    """Образец не подходит для анализа"""
    def __init__(self, text):
        self.txt = text


def normalize(atoms):
    """Приведение образца в нормальную форму (только для линейных)"""
    norm_atoms = []
    e_index = 0

    for i in range(len(atoms)):

        if atoms[i].type == 'e':
            if i < len(atoms) - 1:
                if atoms[i+1].type == 'e':
                    continue
            norm_atoms.append(Atom('e.' + str(e_index)))
            e_index += 1

        elif atoms[i].type == 'tf':
            if i > 0:
                if atoms[i-1].type != 'e':
                    norm_atoms.append(Atom('e.' + str(e_index)))
                    e_index += 1
            else:
                norm_atoms.append(Atom('e.' + str(e_index)))
                e_index += 1

            norm_atoms.append(atoms[i])

            if i < len(atoms) - 1:
                if atoms[i+1].type != 'e':
                    norm_atoms.append(Atom('e.' + str(e_index)))
                    e_index += 1
            else:
                norm_atoms.append(Atom('e.' + str(e_index)))
                e_index += 1

        else:
            norm_atoms.append(atoms[i])

    return norm_atoms


def t_exist(atoms):
    for atom in atoms:
        if atom.type == 't':
            return True
    return False


def t_float_exist(atoms):
    for atom in atoms:
        if atom.type == 'tf':
            return True
    return False


def t_float_combine(atoms):
    """Обнаружение и маркировака плавающих t"""

    def test_neighbors(atoms, index, counter):
        i = index + 1
        while i < len(atoms):
            if (atoms[i].type == 't' and counter[atoms[i].val] > 1) or atoms[i].type in ['c', 'c']:
                i = len(atoms)
            elif atoms[i].type == 'e':
                return False
            i += 1

        i = index - 1
        while i >= 0:
            if (atoms[i].type == 't' and counter[atoms[i].val] > 1) or atoms[i].type in ['c', 'c']:
                i = -1
            elif atoms[i].type == 'e':
                return False
            i -= 1
        return True

    t_counter = Counter()
    for atom in atoms:
        if atom.type == 't':
            t_counter[atom.val] += 1

    result = False
    for i in range(len(atoms)):
        if atoms[i].type == 't':
            if t_counter[atoms[i].val] > 1:
                continue
            else:
                if not test_neighbors(atoms, i, t_counter):
                    atoms[i].type = 'tf'
                    result = True
    return result


def is_linear(atoms):
    """Проверка образца на линейность"""
    es = set()
    for atom in atoms:
        if atom.type == 'e' and atom.val in es:
            return False
        es.add(atom.val)
    return True


def tfe_to_v(atoms):
    """Замена пар (плавающая t, e) на v"""
    atomsv = []
    i = 0
    while i < len(atoms):
        if atoms[i].type == 'e':
            if i < len(atoms) - 1:
                if atoms[i+1].type == 'tf':
                    atomsv.append(atoms[i])
                    atomsv[-1].type = 'v'
                    i += 1
                if i < len(atoms) - 1 and atoms[i+1].type == 'e':
                    i += 1
        if atoms[i].type == 'tf':
            if i < len(atoms) - 1 and atoms[i + 1].type == 'e':
                atomsv.append(atoms[i])
                atomsv[-1].type = 'v'
                i += 1
        else:
            atomsv.append(atoms[i])
        i += 1

    return atomsv


def s_to_c(p):
    """Замена s на свежие константы"""
    s_index = 0
    s_dict = {}
    for i in range(len(p)):
        if p[i].type == 's':
            if p[i] not in s_dict:
                s_dict[p[i]] = 'C.' + str(s_index)
                s_index += 1
            p[i] = Atom(s_dict[p[i]])


def get_N(p):
    """Поиск максимальной длины подслова из t"""
    N, temp_n = 0, 0
    for atom in p:
        if atom.type in ('t', 'tf'):
            temp_n += 1
        else:
            N = max(N, temp_n)
            temp_n = 0
    return N
