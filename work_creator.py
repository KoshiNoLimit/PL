import re


FUNC = re.compile('\n[a-zA-Z]+ \\{[^\\}]+\\}')
ATOM = re.compile('\'[^\']*\'')


def program_to_works(program_path):
    funcs = funcs_from_file(program_path)
    pattern_groups = [patters_from_func(f) for f in funcs]
    work_pairs = []
    for group in pattern_groups:
        for i in range(len(group)):
            for j in range(i+1, len(group)):
                work_pairs.append((group[i], group[j]))


def patters_from_func(func):
    sentences = func.split('\n')[2:-1]
    samples = [s.split(' = ')[0].strip() for s in sentences]
    return samples


def funcs_from_file(path):
    with open(path) as f:
        return FUNC.findall(f.read())
