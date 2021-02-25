from algorithm.atom import *
import algorithm.pattern_format as pf
from algorithm.substitution import *
from collections import Counter
import logging

logging.basicConfig(level=logging.DEBUG)


def NePL_method(p1, p2):
    logging.debug('NePL: ' + str(p1) + str(p2))
    p1 = pf.normalize(p1)

    N = pf.get_N(p1)
    p1 = pf.tfe_to_v(p1)
    q = get_Q(p2, N)
    subs = ConstSubstitution(q, p1)
    return subs.algorithm()


def NePL_test(p1, p2):
    """Проверка на возможность применения NePL метода"""
    for p in (p1, p2):
        if not pf.t_float_exist(p):
            continue
        for i in range(len(p)):
            if p[i].type == 'e':
                if i > 0 and p[i - 1].type == 'tf':
                    continue
                if i < len(p) - 1 and p[i + 1].type == 'tf':
                    continue
                return False

    # Дополнительно требуем, чтобы повторные вхождения t и s в P1 не разделялись вхождением e-переменной
    val_free = set()
    val_splited = set()
    for atom in p1:
        if atom.type in ('t', 's'):
            if atom.val in val_splited:
                return False
            val_free.add(atom.val)
        elif atom.type == 'e':
            val_splited.update(val_free)

    return True


def EPL_method(p1, p2):
    logging.debug('EPL: ' + str(p1) + str(p2))
    p1 = pf.normalize(p1)

    N = pf.get_N(p1)
    q = get_Q(p2, N)
    logging.debug(str(p1) + str(q))

    subs = ConstSubstitution(q, p1)
    return subs.algorithm()


def not_linear_method(p1, p2):
    """Метод для сопоставления образцов с кратными e-переменными"""
    logging.debug('NotLinear: ' + str(p1) + str(p2))
    subs = PToPSubstitution(p1, p2)
    return subs.algorithm()


def bruteforce_algorithm(p1, p2):
    """Переборный алгоритм"""
    e_cnt = pf.e_normalize(p2)
    pf.s_to_c(p2)
    logging.debug('BF: ' + str(p1) + str(p2))
    split_subs = SplitSubstitution(p1, p2, EPL_method).algorithm()
    logging.debug('SplitSubstitution: ' + str(split_subs))
    if len(split_subs) == 0:
        return False

    e_subs = []
    for sub in split_subs:
        e_subs.extend(TruncatedMap(e_cnt).algorithm(sub, p2))

    logging.debug('\nSubs of e: ' + str(e_subs))

    subs_list = pf.get_subatom_sets(e_subs, e_cnt)

    # if set() in subs_list:
    #     return True

    print('Sets of SubAtoms:', subs_list)

    fix_point = False
    while not fix_point:
        subs_list, fix_point = pf.subatom_simplification(subs_list)

    print('Simplification: ', subs_list)
    return set() in subs_list


def enclosure_check(p1, p2):
    """Алгоритм проверки вложения образцов"""
    p1, p2 = atomize_sample(p1), atomize_sample(p2)

    if not pf.is_linear(p1) or not pf.is_linear(p2):
        return not_linear_method(p1, p2)

    if pf.t_exist(p1):
        if pf.t_float_combine(p1):

            if NePL_test(p1, p2):
                return NePL_method(p1, p2)

            return bruteforce_algorithm(p1, p2)

    return EPL_method(p1, p2)
