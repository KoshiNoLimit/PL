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
    """Проверка на наличие плавающих t-переменных"""

    def test_neighbor(atoms, index, counter):
        if atoms[index].type == 'e':
            return False
        elif atoms[index].type == 't' and counter[atoms[index].val] < 2:
            return False
        elif atoms[index].type == 'tf':
            return False
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
                if i > 0:
                    if not test_neighbor(atoms, i - 1, t_counter):
                        atoms[i].type = 'tf'
                        result = True
                if i < len(atoms) - 1:
                    if not test_neighbor(atoms, i + 1, t_counter):
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
