import unittest


class Example:
    def __init__(self, pare_of_patters, answer):
        self.ps = pare_of_patters
        self.answer = answer


class EnclosureTest(unittest.TestCase):
    def __init__(self, method):
        super().__init__()
        self.method = method

    def work_tests(self, exs):
        for ex in exs:
            with self.subTest(i=ex):
                self.assertEqual(self.method(ex.ps[0], ex.ps[1]), ex.answer, msg=ex.ps)

    def without_t(self):
        """Проверка на образцах без t"""
        examples = [
            Example(
                ('e.Var',
                 'Iams c re en ed'), True),
            Example(
                ('e.X A e.Y',
                 'e.X'), False),
        ]
        self.work_tests(examples)

    def with_repeated_t(self):
        """Проверка на образцах с кратными t-переменными"""
        examples = [
            Example(
                ('t.1 A t.2 e.1 t.1',
                 'e.1 AB e.2 A e.3'), False),
            Example(
                ('t.1 A t.2 e.1 t.1',
                 'B A e.x t.3 A'), False),
            Example(
                ('e.y0 t.y e.y1 t.y1 t.y C e.y2',
                 'C A e.x1 A B C e.x2'), False),
            Example(
                ('t.1 A t.2 e.1 t.1',
                 'B A e.x t.3 B'), True),
            Example(
                ('t.1 A t.2 e.1 t.1',
                 'B A e.x t.3 B A'), False),
        ]
        self.work_tests(examples)

    def with_anchor_t(self):
        """Проверка на образцах с якорными t"""
        examples = [
            Example(
                ('t.x',
                 'A'), True),
        ]
        self.work_tests(examples)

    def with_float_t(self):
        """Проверка на образцах с плавающими t"""
        examples = [
            Example(
                ('t.X1 e.Y1',
                 'e.X2 t.Y2'), True),
            Example(
                ('e.x t.y1 t.y2',
                 'A e.x B'), True)
        ]
        self.work_tests(examples)

    def with_s(self):
        """Проверка на образцах с s"""
        examples = [
            Example(
                ('s.1 s.2',
                 'A B'), True),
            Example(
                ('s.1 e.x s.2',
                 's.6 s.5'), True),
            Example(
                ('e.x s.y',
                 's.x. e.y'), False),
        ]
        self.work_tests(examples)

    def with_repeated_s(self):
        """Проверка на образцах с s"""
        examples = [
            Example(
                ('s.1 A s.1',
                 'B A B'), True),
            Example(
                ('s.1 A s.1',
                 'B A A'), False),
            Example(
                ('s.1 e.x s.1',
                 's.3 A s.3'), True),
        ]
        self.work_tests(examples)

    def not_linear(self):
        """Проверка на нелинейных образцах"""
        examples = [
            Example(
                ('e.Z e.Y e.Z',
                 'e.X B B A B e.X B'), True),
            Example(
                ('e.1 e.2 e.2 e.1',
                 'A B A'), False),
            Example(
                ('e.1 e.2 e.2 e.1',
                 'e.1 e.2 e.1'), False),
            Example(
                ('e.1 e.2 e.2 e.1',
                 'ABA'), False),
        ]
        self.work_tests(examples)


class WorkCreatingTest(unittest.TestCase):
    """Проверка правильности нахождения образцов в коде программы"""
    def __init__(self, method):
        super().__init__()
        self.method = method

    def programs_to_works(self):
        examples = []
        for ex in examples:
            with self.subTest(i=ex):
                self.assertEqual(self.method(ex.ps[0], ex.ps[1]), ex.aswer)
