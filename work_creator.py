import re
from sys import argv
from algorithm.enclosure import enclosure_check


FUNC = re.compile('[a-zA-Z]+ \\{[^\\}]+\\}')
ATOM = re.compile('\'[^\']*\'')


def program_to_works(program_path):
    funcs = funcs_from_file(program_path)
    pattern_groups = [patters_from_func(f) for f in funcs]
    work_pairs = []
    for group in pattern_groups:
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                work_pairs.append((group[i], group[j]))
    return work_pairs


def patters_from_func(func):
    sentences = list(filter(lambda s: '=' in s, func.split('\n')))

    samples = [s.split(' = ')[0].strip() for s in sentences]
    if not(2 <= len(samples) <= 10):
        raise Exception('Неподходящее кол-во предложений')
    return samples


def funcs_from_file(path):
    with open(path) as f:
        return FUNC.findall(f.read())


if __name__ == '__main__':
    works = program_to_works(argv[1])
    for work in works:
        print('[' + str(work[0]) + '] [' + str(work[1]) + '] : ' + str(enclosure_check(work[0], work[1])))
