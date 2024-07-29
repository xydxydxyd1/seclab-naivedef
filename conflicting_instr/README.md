# Conflicting Instructions

This folder contains the code for examining the following factors relating to
conflicting instructions.

* Position: In progress
* Format: Incomplete

# Code

The code is separated into three steps: Test generation (`gen_test`), execution
and judging (`judge`), and examination (`examine`). Data is transferred via
a single master DataFrame pickle from one stage to another.

## Test generation

Each generator file (such as `position.py`) has a `gen_testcase` function
that outputs a dataframe with the following columns:

- full\_prompt (str)
- task\_1 (str)
- output\_1 (str): The expected output of Task 1
- task\_2 (str)
- output\_2 (str): The expected output of Task 2, which needs to be different
  from `output_1`

The test dataframe will then be pickled and saved according to arguments
provided to `main.py`

# Execute and judge

The judging stage produces the following columns:

- response (str): The response of the model (GPT3.5)
- match (int): `1` if the response is an exact match of `output_1`, `2` if the
  response is an exact match of `output_2`, and `0` if otherwise.
