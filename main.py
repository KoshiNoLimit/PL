from algorithm.enclosure import enclosure_check
from tests import EnclosureTest, WorkCreatingTest
from algorithm.atom import *
from algorithm.substitution import *
en_test = EnclosureTest(enclosure_check)
en_test.without_t()
en_test.with_anchor_t()
en_test.with_float_t()
en_test.not_linear()
en_test.with_s()
en_test.with_repeated_s()
en_test.with_repeated_t()

# tm = TruncatedMap(2)
# p1, p2 = atomize_sample('e.1 t.y1 A C e.3'), atomize_sample('e.0 A B C e.1')
# pf.t_float_combine(p1)
# print(tm.algorithm(p1, p2))

# tm = TruncatedMap(1)
# p1, p2 = atomize_sample('В А t.1 e.1 B'), atomize_sample('B A e.2 t.2 B')
# pf.t_float_combine(p1)
# print(tm.algorithm(p1, p2))
