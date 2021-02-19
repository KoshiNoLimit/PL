from algorithm.atom import *
import algorithm.pattern_format as pf
from algorithm.substitution import Substitution, PToPSubstitution


def get_N(atoms):
    """Поиск максимальной длины подслова из t"""
    N, temp_n = 0, 0
    for atom in atoms:
        if atom.type in ('t', 'tf'):
            temp_n += 1
        else:
            N = max(N, temp_n)
            temp_n = 0
    return N


def get_Q(atoms, N):
    """Создание подстановки"""
    q = []
    for atom in atoms:

        if atom.type == 'e' or atom.type == 'v':
            for i in range(N+1):
                q.append('A.'+atom.val[2:]+str(i))

        elif atom.type == 't':
            q.append('B.' + atom.val[2:])

        elif atom.type == 's':
            q.append('C.' + atom.val[2:])

        elif atom.type == 'c':
            q.append(atom.val)

        else:
            raise pf.PatternException('Unknown type: ' + atom.type)

    return q


def NePL_method(atoms1, atoms2):
    atoms1 = pf.normalize(atoms1)

    N = get_N(atoms1)
    atoms1 = pf.tfe_to_v(atoms1)
    q = get_Q(atoms2, N)
    subs = Substitution(q, atoms1)
    return subs.algorithm()


def NePL_test(atoms1, atoms2):
    """Проверка на возможность применения NePL метода"""
    for atoms in (atoms1, atoms2):
        if not pf.t_float_exist(atoms):
            continue
        for i in range(len(atoms)):
            if atoms[i].type == 'e':
                if i > 0 and atoms[i-1].type == 'tf':
                    continue
                if i < len(atoms)-1 and atoms[i+1].type == 'tf':
                    continue
                return False

    # Дополнительно требуем, чтобы повторные вхождения t в P1 не разделялись вхождением e-переменной
    # t_free = set()
    # t_splited = set()
    # for atom in atoms1:
    #     if atom.type in ('t', 'tf'):
    #         if atom.val in t_splited:
    #             return False
    #         t_free.add(atom.val)
    #     elif atom.type == 'e':
    #         t_splited.update(t_free)

    return True


def EPL_method(atoms1, atoms2):
    atoms1 = pf.normalize(atoms1)

    N = get_N(atoms1)
    q = get_Q(atoms2, N)

    subs = Substitution(q, atoms1)
    return subs.algorithm()


def not_linear_method(atoms1, atoms2):
    """Метод для сопоставления образцов с кратными e-переменными"""
    subs = PToPSubstitution(atoms1, atoms2)
    return subs.algorithm()


def enclosure_check(p1, p2):
    """Алгоритм проверки вложения образцов"""
    atoms1, atoms2 = atomize_sample(p1), atomize_sample(p2)

    if not pf.is_linear(atoms1) or not pf.is_linear(atoms2):
        return not_linear_method(atoms1, atoms2)

    if pf.t_exist(atoms1):
        if pf.t_float_combine(atoms1):
            if not NePL_test(atoms1, atoms2):
                print("Algorithm wasn't learned to work with patterns like these")
                return False

            return NePL_method(atoms1, atoms2)

    return EPL_method(atoms1, atoms2)
