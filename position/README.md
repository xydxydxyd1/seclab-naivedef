The code is separated into two steps: attack generation and evaluation. This is
because the evaluation should be the same for all the hypotheses: which
instruction is favored. I will not handle more than 2 instructions.

# Test case generation

Each generator file (such as `position.py`) has a `gen_testcase` function
that outputs an array of TestCase objects with the following properties:

- full\_prompt (str)
- task\_1 (str)
- output\_1 (str): The expected output of Task 1
- task\_2 (str)
- output\_2 (str): The expected output of Task 2
