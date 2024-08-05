# Factory for Tests

from generator.position import PositionTest

test_dict = {
    'position': PositionTest,
    'format_capitalize': None
}

test_choices = test_dict.keys()

def get_test(test_name):
    return test_dict[test_name]

