import re


FUNC = re.compile('\n[a-zA-Z]+ \\{[^\\}]+\\}')
ATOM = re.compile('\'[^\']*\'')


def samples_from_func(func):
    sentences = func.split('\n')[2:-1]

    samples = [s.split(' = ')[0].strip() for s in sentences]

    return samples


def funcs_from_file(path):
    with open(path) as f:
        return FUNC.findall(f.read())
