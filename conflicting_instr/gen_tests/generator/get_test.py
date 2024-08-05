# Factory for Tests

from generator.position import PositionTest
from generator.position_filler import PositionFillerTest

test_dict = {
    'position': PositionTest,
    'position_filler': PositionFillerTest,
    'format_capitalize': None
}

test_choices = test_dict.keys()

def get_test(test_name):
    return test_dict[test_name]

