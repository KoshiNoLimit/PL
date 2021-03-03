import re
from sys import argv
from algorithm.enclosure import enclosure_check
import csv
import logging


FUNC = re.compile('\S+ \\{[^\\}]+\\}')
ATOM = re.compile('\'[^\']*\'')


class Function:
    def __init__(self, text):
        self.name, self.body = text.split(' ', 1)
        self.patterns = self._find_patterns()

    def _find_patterns(self):
        sentences = list(filter(lambda s: '=' in s, self.body.split('\n')))
        return [s.split(' = ')[0].strip()[1:-1] for s in sentences]

    @property
    def work_pairs(self):
        pairs = []
        for i in range(len(self.patterns)):
            for j in range(i+1, len(self.patterns)):
                pairs.append((self.patterns[i], self.patterns[j]))
        return pairs

    def __str__(self):
        return self.name + ' ' + self.body

    def __repr__(self):
        return self.name


def program_to_works(path):
    logging.info('\033[34mStart with ' + path + '\033[37m')
    funcs = funcs_from_file(path)

    with open(path[:-4] + '_results.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['function', 'pattern1', 'pattern2', 'result'])
        for f in funcs:
            logging.info('Work function' + f.name)
            for pair in f.work_pairs:
                writer.writerow([f.name, pair[0], pair[1], enclosure_check(pair[0], pair[1])])


def funcs_from_file(path):
    with open(path) as f:
        return tuple(map(
            lambda x: Function(x),
            FUNC.findall(f.read())))


if __name__ == '__main__':
    program_to_works(argv[1])
