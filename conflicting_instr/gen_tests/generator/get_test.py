# Factory for Tests

from position import PositionTest

test_dict = {
    'position': PositionTest,
    'format_capitalize': None
}

def get_test(test_name):
    return test_dict[test_name]
