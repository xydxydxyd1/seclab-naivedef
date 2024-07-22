import argparse

# Import generation methods
from position import gen_testcase as gen_test_pos

GENERATOR_DICT = {
    'position': gen_test_pos
}


def parse_args():
    """Terminal interface"""
    parser = argparse.ArgumentParser(
        description='Generate test cases for conflicting isntructions experiment'
    )
    parser.add_argument(
        'output_path', type=str, help='Path to the file to save the generated test cases.'
    )
    parser.add_argument(
        'type', type=str, help='Which type of test case to generate',
        choices=GENERATOR_DICT.keys()
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    output_path = args.output_path
    generator = GENERATOR_DICT[args.type]
    for testcase in generator():
        print(testcase)
