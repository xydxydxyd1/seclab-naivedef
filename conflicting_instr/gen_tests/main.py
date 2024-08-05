import argparse
import logging

from generator.get_test import get_test, test_choices


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
        choices=test_choices, default='position'
    )
    parser.add_argument(
        '--num_tests', type=int, help='The number of tests to run', default=100
    )
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='main.log', filemode='w')
    args = parse_args()
    output_path = args.output_path
    test = get_test(args.type)()

    test.gen_tests(args.num_tests);
    test_df = test.tests()

    print(test_df)
    print(f"Saving test cases to {output_path}")
    test_df.to_pickle(output_path)
