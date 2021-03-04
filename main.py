from algorithm.enclosure import enclosure_check
from unit_tests import EnclosureTest
from work_creator import program_to_works
import logging


logging.basicConfig(level=logging.INFO)


def unit_tests_run():
    en_test = EnclosureTest(enclosure_check)
    en_test.without_t()
    en_test.with_anchor_t()
    en_test.with_float_t()
    en_test.not_linear()
    en_test.with_s()
    en_test.with_repeated_s()
    en_test.with_repeated_t()


def code_tests_run():
    refal_files = ['refal examples/test{}.ref'.format(i) for i in range(1, 11)]

    for file in refal_files:
        program_to_works(file)


code_tests_run()
# unit_tests_run()