The code is separated into two steps: attack generation and evaluation. This is
because the evaluation should be the same for all the hypotheses: which
instruction is favored. I will not handle more than 2 instructions.

# Attack generation

Each attack generation file (such as `position.py`) has a `gen_atk` function
that outputs an object of the following:

- full\_prompt (str)
- task\_1 (str)
- task\_2 (str)
- output\_1 (str): The expected output of Task 1
- output\_2 (str): The expected output of Task 2
