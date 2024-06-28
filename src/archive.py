# Generate and save evaluation prompts
import numpy as np
import pandas as pd
from generate_attacks import TASKS

import argparse
import logging


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("tests_path", type=str,
                        help="Path to the tests to be conducted")
    return parser.parse_args()


def read_tests(tests_path):
    """Read tests from the given path"""
    return pd.read_pickle(tests_path)


def generate_evaluations(tests):
    """Generate evaluations for the given tests from generate_attacks"""
    evaluations = []
    for test in tests.loc[:, "fullPrompt"]:
        evaluation = f"Please evaluate the following prompt: {test}"
        evaluations.append(evaluation)
    return evaluations


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename='generate_evaluations.log', filemode='w')

    args = parse_args()
