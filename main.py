from work_creator import program_to_works
from algorithm.enclosure import enclosure_check
from tests import EnclosureTest, WorkCreatingTest

en_test = EnclosureTest(enclosure_check)
en_test.without_t()
en_test.with_anchor_t()
en_test.with_float_t()
en_test.not_linear()
en_test.with_repeated_t()
en_test.with_s()
en_test.with_repeated_s()

# cr_test = WorkCreatingTest(program_to_works)
# cr_test.programs_to_works()
