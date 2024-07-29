import argparse
import logging

# Import test generators methods
from generator.position import gen_testcase as gen_test_pos
from generator.format_capitalize import gen_testcase as gen_test_fmt_cap

GENERATOR_DICT = {
    'position': gen_test_pos,
    'format_capitalize': gen_test_fmt_cap
}


def parse_args():
    """Terminal interface"""
    parser = argparse.ArgumentParser(
        description='Generate test cases for conflicting isntructions experiment'
    )
    parser.add_argument(
        '--output_path', type=str, help='Path to the file to save the generated test cases.',
        default='../data/gen_tests.pkl'
    )
    parser.add_argument(
        '--type', type=str, help='Which type of test case to generate',
        choices=GENERATOR_DICT.keys(), default='format_capitalize'
    )
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='main.log', filemode='w')
    args = parse_args()
    output_path = args.output_path
    generator = GENERATOR_DICT[args.type]
    testcases = generator()

    print(testcases)
    print(f"Saving test cases to {output_path}")
    testcases.to_pickle(output_path)
