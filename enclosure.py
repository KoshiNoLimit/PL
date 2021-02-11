from atom import *
import pattern_format as pf


def subs(const, pattern):
    """Алгоритм сопоставления константного выражения с образцом"""
    pass


def get_N(atoms):
    """Поиск максимальной длины подслова из t"""
    N, temp_n = 0, 0
    for atom in atoms:
        if atom.type == 't':
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
                q.append('A'+atom.val[2:]+str(i))

        elif atom.type == 't':
            q.append('B' + atom.val[2:])

        else:
            q.append(atom.val)

    return q


def NePL_method(atoms1, atoms2):
    atoms2v = []
    for atom in atoms2:
        if atom.type == 'e':
            continue
        if atom.type == 'tf':
            atom.type = 'v'
        atoms2v.append(atom)

    N = get_N(atoms1)
    q = get_Q(atoms2, N)

    return subs(q, atoms1)


def NePL_test(atoms1, atoms2):
    """Проверка на возможность применения NePL метода"""
    for atoms in (atoms1, atoms2):
        for i in range(len(atoms)):
            if atoms[i].type == 'e':
                if i > 0 and atoms[i-1].type == 'tf':
                    continue
                if i < len(atoms)-1 and atoms[i+1].type == 'tf':
                    continue
                return False

    # Дополнительно требуем, чтобы повторные вхождения t в P1 не разделялись вхождением e-переменной
    t_free = set()
    t_splited = set()
    for atom in atoms1:
        if atom.type == 't':
            if atom.val in t_splited:
                return False
            t_free.add(atom.val)
        elif atom.type == 'e':
            t_splited.update(t_free)

    return True


def EPL_method(atoms1, atoms2):
    N = get_N(atoms1)
    q = get_Q(atoms2, N)

    return subs(q, atoms1)


def enclosure(p1, p2):
    """Алгоритм проверки вложения образцов"""
    atoms1, atoms2 = atomize_sample(p1), atomize_sample(p2)

    if not pf.is_linear(atoms1) or not pf.is_linear(atoms2):
        raise pf.PatternException('Not linear pattern')

    if pf.t_exist(atoms1):
        fl1, fl2 = pf.t_float_exist(atoms1), pf.t_float_exist(atoms2)
        if fl1:
            if not NePL_test(atoms1, atoms2):
                raise pf.PatternException('Can\'t try NePL and EPL')
            atoms1, atoms2 = pf.normalize(atoms1), pf.normalize(atoms2)
            return NePL_method(atoms1, atoms2)

    atoms1, atoms2 = pf.normalize(atoms1), pf.normalize(atoms2)
    return EPL_method(atoms1, atoms2)
