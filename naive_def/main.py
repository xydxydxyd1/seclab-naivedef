# Main file run
import prompts
import numpy as np
import os
import pandas as pd
import logging
from call_gpt import call_gpt
from generate_attacks import TASKS

logger = logging.getLogger(__name__)
DEFAULT_ATTACKS_PATH = "data/attacks.bin"
DEFAULT_RESPONSES_PATH = "data/responses.bin"
DEFAULT_EVAL_PATH = "data/evals.bin"
MOCK = False


def setup():
    """Setup for the program"""
    logging.basicConfig(level=logging.DEBUG, filename='main.log', filemode='w')
    print("Enter and only enter the number for the following prompts")
    pass


def load_test_prompts():
    """Entire process of loading tests. Returns pandas dataframe of tests"""
    # Load testing prompts
    ans = input("1) Load existing test prompts\n2) Generate test prompts\n> ")
    willLoad = ans == "1"
    attackBinPath = ""
    if willLoad:
        # Load test cases
        attackBinPath = input(
            f"Enter the path to the test cases (default is {DEFAULT_ATTACKS_PATH}): ")
        if attackBinPath == "":
            attackBinPath = DEFAULT_ATTACKS_PATH
    else:
        # Generate test cases
        os.system(
            "python3 generate_attacks.py data/instructions.txt data/attacks.bin")
        attackBinPath = DEFAULT_ATTACKS_PATH
    tests = pd.read_pickle(attackBinPath)
    tests = tests.head(100)
    logger.info(f"load_tests: Loaded test cases:\n{tests}")
    return tests


def run_tests(tests):
    """Entire process of running tests. Returns pandas dataframe of tests"""
    if MOCK:
        print("Running tests in MOCK mode")
    else:
        print("Running tests in REAL mode")
    abort = input(f"Run {len(tests)} tests on ChatGPT? (y/n) ") != "y"
    if abort:
        print("Aborting tests")
        exit()

    responses = call_gpt(tests.loc[:, "fullPrompt"], MOCK, verbose=True)
    tests.insert(len(tests.columns), "response", responses)
    logger.info(f"run_tests: Ran tests:\n{tests}")
    logger.info(f"run_tests: Responses:\n{tests.loc[:, 'response']}")
    return tests


def save_responses(tests):
    """Entire process of saving responses. Returns pandas dataframe of tests"""
    # Save responses
    savePath = input(f"Save path (default is {DEFAULT_RESPONSES_PATH}): ")
    if savePath == "":
        savePath = DEFAULT_RESPONSES_PATH
    tests.to_pickle(savePath)
    logger.info(f"save_responses: Saved responses to {savePath}")
    return tests


def get_responses():
    """Entire process of loading or generating responses. Returns pandas
    dataframe of responses"""
    will_call_gpt = input(
        "1) Load existing responses\n2) Generate new prompts\n> ")

    if will_call_gpt == "1":
        responsePath = input(
            f"Enter the path to the responses (default is {DEFAULT_RESPONSES_PATH}): ")
        if responsePath == "":
            responsePath = DEFAULT_RESPONSES_PATH
        responses = pd.read_pickle(responsePath)
    else:
        tests = load_test_prompts()
        # tests = tests.head(5)
        run_tests(tests)
        save_responses(tests)
        responses = tests
    logger.info(f"get_responses: Got responses:\n{responses}")
    return responses


def make_eval_prompts(tests):
    """Entire process of loading evaluations. Returns pandas dataframe of
    evaluations"""
    tests.insert(len(tests.columns), "systemAlignment", np.empty(len(tests)))
    tests.insert(len(tests.columns), "adversaryAlignment", np.empty(len(tests)))
    tests.insert(len(tests.columns), "conflict", np.empty(len(tests)))
    for i in range(tests.shape[0]):
        test = tests.iloc[i]
        tests.loc[i, "systemAlignment"] = prompts.SYSTEM_ALIGNMENT_PROMPT.format(
            system_task=TASKS[test["taskId"]],
            unmodified_adversary_task=test["unmodifiedAdversaryTask"],
            response=test["response"]
        )
        tests.loc[i, "adversaryAlignment"] = prompts.ADVERSARY_ALIGNMENT_PROMPT.format(
            unmodified_adversary_task=test["unmodifiedAdversaryTask"],
            response=test["response"]
        )
        tests.loc[i, "conflict"] = prompts.CONFLICT_DETECTION_PROMPT.format(
            response=test["response"]
        )
    logger.info(f"make_eval_prompts: Made evaluations:\n{
                tests.loc[:, ['systemAlignment', 'adversaryAlignment', 'conflict']]}")
    return tests


def call_eval_prompts(tests):
    """Entire process of calling evaluations. Returns pandas dataframe of
    evaluations"""
    if MOCK:
        print("Running evaluations in MOCK mode")
    else:
        print("Running evaluations in REAL mode")
    abort = input(
        f"Run {len(tests)*3} evaluations on ChatGPT? (y/n) ") != "y"
    if abort:
        print("Aborting evaluations")
        exit()

    responses = call_gpt(tests.loc[:, "systemAlignment"], MOCK, verbose=True)
    tests.insert(len(tests.columns), "systemAlignmentResponse", responses)
    responses = call_gpt(tests.loc[:, "adversaryAlignment"], MOCK, verbose=True)
    tests.insert(len(tests.columns), "adversaryAlignmentResponse", responses)
    responses = call_gpt(tests.loc[:, "conflict"], MOCK, verbose=True)
    tests.insert(len(tests.columns), "conflictResponse", responses)
    logger.info(f"call_eval_prompts: Ran evaluations:\n{tests}")
    return tests


def save_evals(tests):
    """Entire process of saving evaluations. Returns pandas dataframe of
    evaluations"""
    savePath = input(f"Save path for evaluations (default is {DEFAULT_EVAL_PATH}): ")
    if savePath == "":
        savePath = DEFAULT_EVAL_PATH
    tests.to_pickle(savePath)
    logger.info(f"save_evals: Saved evaluations to {savePath}")
    return tests


def get_evals(tests):
    """Entire process of loading or generating evaluations. Returns pandas
    dataframe of evaluations"""
    tests = make_eval_prompts(tests)
    tests = call_eval_prompts(tests)
    tests = save_evals(tests)
    logger.info(f"get_evals: Got evaluations:\n{tests}")
    return tests


if __name__ == "__main__":
    setup()

    tests = get_responses()
    tests = get_evals(tests)
    print(tests)
    # Visualize and save
