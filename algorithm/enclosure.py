from algorithm.atom import *
import algorithm.pattern_format as pf
from algorithm.substitution import *
import logging

# logging.basicConfig(level=logging.DEBUG)


def enclosure_check(p1, p2):
    """Алгоритм проверки вложения образцов"""
    p1, p2 = atomize_sample(p1), atomize_sample(p2)

    if not pf.is_linear(p1) or not pf.is_linear(p2):
        return not_linear_method(p1, p2)

    if pf.t_exist(p1):
        if pf.t_float_combine(p1):

            if pf.NePL_test(p1, p2):
                return NePL_method(p1, p2)

            return bruteforce_method(p1, p2)

    return EPL_method(p1, p2)


def NePL_method(p1, p2):
    """Метод для нестирающего языка"""
    logging.debug('NePL: ' + str(p1) + str(p2))
    p1 = pf.normalize(p1)

    N = pf.len_max_t_subword(p1)
    p1 = pf.tfe_to_v(p1)
    q = ConstSubstitution.build(p2, N)
    subs = ConstSubstitution(q, p1)
    return subs.algorithm()


def EPL_method(p1, p2):
    """Метод для стирающего языка"""
    logging.debug('EPL: ' + str(p1) + str(p2))
    p1 = pf.normalize(p1)

    N = pf.len_max_t_subword(p1)
    q = ConstSubstitution.build(p2, N)
    logging.debug(str(p1) + str(q))

    subs = ConstSubstitution(q, p1)
    return subs.algorithm()


def not_linear_method(p1, p2):
    """Метод сопоставления образцов с кратными _e-переменными"""
    logging.debug('NotLinear: ' + str(p1) + str(p2))
    subs = PToPSubstitution(p1, p2)
    return subs.algorithm()


def bruteforce_method(p1, p2):
    """Метод полного перебора"""
    e_cnt = pf.e_normalize(p2)
    pf.s_to_c(p2)
    logging.debug('BruteForce: ' + str(p1) + str(p2))
    split_subs = SplitSubstitution(p1, p2, EPL_method).algorithm()
    logging.debug('SplitSubstitution: ' + str(split_subs))
    if len(split_subs) == 0:
        return False

    e_subs = []
    for sub in split_subs:
        e_subs.extend(TruncatedMap(e_cnt).algorithm(sub, p2))

    logging.debug('\nESubstitution: ' + str(e_subs))

    # if set() in e_subs:
    #     return True

    if len(e_subs) == 0:
        for sub in split_subs:
            if NePL_method(sub, p2):
                return True
        return False

    subs_list = pf.get_subatom_sets(e_subs, e_cnt)

    print('Sets of SubAtoms:', subs_list)

    fix_point = False
    while not fix_point:
        subs_list, fix_point = pf.subatom_simplification(subs_list)

    print('Simplification: ', subs_list)
    return set() in subs_list
