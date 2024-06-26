# Calls GPT with the given tests
import numpy as np
import pandas as pd
import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv

import logging
from pprint import pformat

load_dotenv()
logger = logging.getLogger(__name__)

client = OpenAI(organization=os.environ.get("OPENAI_ORG_ID"))


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("tests_path", type=str,
                        help="Path to the tests to be conducted")
    return parser.parse_args()


def read_tests(tests_path):
    """Read tests from the given path"""
    return pd.read_pickle(tests_path)


def call_gpt(test):
    """Call GPT with a given test. Returns the response."""
    #chat_completion = client.chat.completions.create(
    #    model="gpt-3.5-turbo",
    #    messages=[{"role": "user", "content": test}],
    #)
    #return chat_completion.choices[0].message.content
    return f"Test run with prompt: {test}"


def generate_responses(tests):
    """Generate responses for the given tests"""
    prompt = f"Performing the following tests will call GPT with {len(tests)} prompts. Do you want to continue? (y/n) "
    response = input(prompt).strip().lower()
    if response != 'y':
        logger.info("User chose to stop.")
        exit(0)
    responses = []
    for test in tests.loc[:, "fullPrompt"]:
        response = call_gpt(test)
        responses.append(response)
    return responses


def run_tests(tests):
    """Run the given tests"""


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename='call_gpt.log', filemode='w')
    args = parse_args()
    # Tests dataframe containing all generated prompts and their properties
    all_tests = read_tests(args.tests_path)
    tests = all_tests[:5]
    logger.info(f"Running tests subset:\n {tests}")
    responses = generate_responses(tests)
    print(responses[0])
