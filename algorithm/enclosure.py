from algorithm.atom import *
import algorithm.pattern_format as pf
from algorithm.substitution import *
from collections import Counter


def NePL_method(p1, p2):
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
    p1 = pf.normalize(p1)

    N = pf.get_N(p1)
    q = get_Q(p2, N)

    subs = ConstSubstitution(q, p1)
    return subs.algorithm()


def not_linear_method(p1, p2):
    """Метод для сопоставления образцов с кратными e-переменными"""
    subs = PToPSubstitution(p1, p2)
    return subs.algorithm()


def bruteforce_algorithm(p1, p2):
    """Переборный алгоритм"""
    pf.s_to_c(p2)
    subs = SplitSubstitution(p1, p2, EPL_method).algorithm()

    e_subs = set()
    map(lambda sub: e_subs.update(TruncatedMap().algorithm(sub, p2)), subs)

    for sub in e_subs:
        for key, value in sub:
            e_cnt, tf_cnt = 0, 0
            for atom in value:
                if atom.type == 'e':
                    e_cnt += 1
                elif atom.type == 'tf':
                    tf_cnt += 1
            sub[key] = (tf_cnt, bool(e_cnt))

    map(lambda s: set(s.items()), e_subs)

    fix_point = False
    while not fix_point:
        fix_point = True

        for sub in e_subs:
            for e in sub:
                if e[1][0] == 0 and e[1][1]:
                    fix_point = False
                    sub.remove(e)

        e_list = list(e_subs)
        for i in range(len(e_subs)):
            for j in range(i+1, len(e_subs)):
                inner = list(e_list[i] ^ e_list[j])
                if len(inner) == 2 and inner[0][0] == inner[1][0]:
                    if inner[0][1][1] and inner[1][1][1]:
                        fix_point = False
                        new_set = e_list[i] & e_list[j]
                        new_set.add((inner[0][0], (min(inner[0][1][0], inner[1][1][0]), True)))
                        e_subs.remove(e_list[i])
                        e_subs.remove(e_list[j])
                        e_subs.add(new_set)

        e_list = list(e_subs)
        for i in range(len(e_subs)):
            for j in range(i + 1, len(e_subs)):
                inner = list(e_list[i] ^ e_list[j])
                if len(inner) == 2 and inner[0][0] == inner[1][0]:
                    if abs(inner[0][1][0] - inner[1][1][0]) == 1:
                        if inner[0][1][0] > inner[1][1][0]:
                            big, small = inner[0], inner[1]
                        else:
                            big, small = inner[1], inner[0]
                        if big[1][1] and not small[1][1]:
                            fix_point = False
                            new_set = e_list[i] & e_list[j]
                            new_set.add((inner[0][0], (small[1][0], True)))
                            e_subs.remove(e_list[i])
                            e_subs.remove(e_list[j])
                            e_subs.add(new_set)

    return e_subs == set(set())


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
