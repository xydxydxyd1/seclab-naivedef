# Calls GPT with the given tests
import os
import numpy as np
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(organization=os.environ.get("OPENAI_ORG_ID"))


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("tests_path", type=str,
                        help="Path to the tests to be conducted")
    return parser.parse_args()


def read_tests(tests_path):
    """Read tests from the given path"""
    return np.loadtxt(tests_path, delimiter=',', quotechar='"')


def call_gpt(test):
    """Call GPT with a given test. Returns the response."""
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": test}],
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    args = parse_args()
    #tests = read_tests(args.tests_path)
    print(call_gpt("Hello, how are you?"))
