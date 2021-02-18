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
                 'Iamscreened'), True),
            Example(
                ('e.X A e.Y',
                 'e.X'), False),
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
