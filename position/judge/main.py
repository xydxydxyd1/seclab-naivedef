# Calls GPT and judges the response
import argparse
from chatgpt import call_gpt
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="ChatGPT")
    parser.add_argument("test_path", type=str, help="Path to the test pickle")
    parser.add_argument("output_path", type=str, help="Path to save response pickle")
    return parser.parse_args()


def judge(test_cases):
    """Judge a test cases' response based on exact match of its two output
    columns. Adds a column to the test_cases DataFrame indicating whether output
    1 (1) or output 2 (2) is matched. If neither is matched, the value is 0."""
    match_1 = test_cases.loc[:, 'response'] == test_cases.loc[:, 'output_1']
    match_2 = test_cases.loc[:, 'response'] == test_cases.loc[:, 'output_2']
    match = np.empty(test_cases.shape[0], dtype=int)
    match[match_1] = 1
    match[match_2] = 2
    test_cases.insert(test_cases.shape[1], 'match', match)

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, filename='main.log', filemode='w')
    args = parse_args()

    test_cases = pd.read_pickle(args.test_path)

    responses = call_gpt(test_cases.loc[:, 'full_prompt'], False, True)
    test_cases.insert(test_cases.shape[1], 'response', responses)

    judge(test_cases)
    
    test_cases.to_pickle(args.output_path)
