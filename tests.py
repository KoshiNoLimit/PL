import unittest


class Example:
    def __init__(self, pare_of_patters, answer):
        self.ps = pare_of_patters
        self.answer = answer


class EnclosureTest(unittest.TestCase):
    def __init__(self, method):
        super().__init__()
        self.method = method

    def without_t(self):
        """Проверка на образцах без t"""
        examples = []
        for ex in examples:
            with self.subTest(i=ex):
                self.assertEqual(self.method(ex.ps[0], ex.ps[1]), ex.aswer)

    def with_anchor_t(self):
        """Проверка на образцах с якорными t"""
        examples = []
        for ex in examples:
            with self.subTest(i=ex):
                self.assertEqual(self.method(ex.ps[0], ex.ps[1]), ex.aswer)

    def with_float_t(self):
        """Проверка на образцах с плавающими t"""
        examples = []
        for ex in examples:
            with self.subTest(i=ex):
                self.assertEqual(self.method(ex.ps[0], ex.ps[1]), ex.aswer)


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
