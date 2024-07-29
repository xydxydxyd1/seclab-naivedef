# Calls GPT with the given tests
import time
import os
import argparse
import pandas as pd
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

from prompts import ADVERSARY_ALIGNMENT_PROMPT, SYSTEM_ALIGNMENT_PROMPT, CONFLICT_DETECTION_PROMPT
from generate_attacks import TASKS, get_instructions

import logging

load_dotenv()
logger = logging.getLogger(__name__)
client = OpenAI(organization=os.environ.get("OPENAI_ORG_ID"))


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("tests_path", type=str,
                        help="Path to the tests to be conducted")
    parser.add_argument("instruction_path", type=str,
                        help="Path to the file containing the instructions")
    return parser.parse_args()


def read_tests(tests_path):
    """Read tests from the given path"""
    return pd.read_pickle(tests_path)


def call_gpt(prompts, mock, verbose=False):
    """Call GPT with given array of tests. Returns an array of responses."""
    start_time = time.time()
    responses = np.empty(len(prompts), dtype=object)
    for i, prompt in enumerate(prompts):
        if mock:
            responses[i] = f"Mock response to prompt: {prompt}"
            continue
        logger.info(f"call_gpt: calling prompt: {prompt}")
        completion = client.chat.completions.create(
           model="gpt-3.5-turbo",
           messages=[{"role": "user", "content": prompt}],
        )
        response = completion.choices[0].message.content
        logger.info(f"Completion: received response: {response}")
        if verbose:
            print(f"Prompt: {prompt}\nResponse: {response}")
        responses[i] = response
    logger.info(f"call_gpt: completed in {time.time() - start_time} seconds.")
    if verbose:
        print(f"Completed in {time.time() - start_time} seconds.")
    return responses


def generate_responses(tests):
    """Generate responses for the given tests"""
    prompt = f"Performing the following tests will call GPT with {
        len(tests)} prompts. Do you want to continue? (y/n) "
    response = input(prompt).strip()
    if response != 'y':
        logger.info("User chose to stop.")
        exit(0)
    responses = []
    for test in tests.loc[:, "fullPrompt"]:
        response = call_gpt(test)
        responses.append(response)
    return responses


def run_tests(tests, instructions):
    """Run the given tests"""
    metrics = ["systemAlignment", "adversaryAlignment", "conflictDetection"]
    results = pd.DataFrame(columns=["response"] + metrics)
    results.loc[:, "response"] = generate_responses(tests)

    # Evaluate responses
    taskIds = tests.loc[:, "taskId"]
    instrIds = tests.loc[:, "instrId"]
    for i, row in results.iterrows():
        response = row["response"]
        task = TASKS[taskIds[i]]
        instruction = instructions[instrIds[i]]
        row["systemAlignment"] = call_gpt(SYSTEM_ALIGNMENT_PROMPT.format(
            system_task=task, unmodified_adversary_task=instruction, response=response))
        row["adversaryAlignment"] = call_gpt(ADVERSARY_ALIGNMENT_PROMPT.format(
            unmodified_adversary_task=instruction, response=response))
        row["conflictDetection"] = call_gpt(CONFLICT_DETECTION_PROMPT.format(
            response=response))
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename='call_gpt.log', filemode='w')
    args = parse_args()
    # Tests dataframe containing all generated prompts and their properties
    all_tests = read_tests(args.tests_path)
    tests = all_tests[:5]
    logger.info(f"Running tests subset:\n {tests}")
    responses = generate_responses(tests)
    instructions = get_instructions(args.instruction_path)
    print(responses[0])
    logger.debug(f"Instructions: {instructions}")
