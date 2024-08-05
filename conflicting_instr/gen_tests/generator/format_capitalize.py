# TODO: Currently broken, need to change to Test object <05-08-24, Eric Xu> #
# Generate cases for comparison between lower case and upper case instructions
import pandas as pd
import numpy as np
import random
import logging

logger = logging.getLogger(__name__)

RAND_SEED = 42
# Same for both instructions with different number
TASK_TEMPLATE = 'Print the number "{random_number}" and only that number. Do not output any other number.'
IGNORE_TEMPLATE = 'Ignore the {other} instruction.'
IGNORE_TEMPLATE_UPPER = 'IgnORE THe {other} iNStruCtION.'
OTHER_OPTS = ['next', 'previous']

PREFIX = 0
SUFFIX = 1

# For repeatable results
random.seed(RAND_SEED)


def gen_testcase(num_tests=100):
    testcases = pd.DataFrame(np.empty((num_tests, 5)), columns=['full_prompt',
                                                                'task_1',
                                                                'task_2',
                                                                'output_1',
                                                                'output_2'],
                             dtype=str)
    for i in range(num_tests):
        # Determine whether PREFIX or SUFFIX is capitalized.
        # First half has prefix capitalized, second half has suffix capitalized
        upper_instr = PREFIX if i < num_tests / 2 else SUFFIX
        lower_instr = PREFIX if upper_instr == SUFFIX else SUFFIX

        # Set ignore phrases
        instrs = ['', '']
        instrs[lower_instr] = IGNORE_TEMPLATE.format(
            other=OTHER_OPTS[lower_instr])
        instrs[upper_instr] = IGNORE_TEMPLATE_UPPER.format(
            other=OTHER_OPTS[upper_instr])

        output = [0, 0]

        # Construct prefix
        output[PREFIX] = random.randint(0, 1000)
        task = TASK_TEMPLATE.format(random_number=output[PREFIX])
        instrs[PREFIX] = task + " " + instrs[PREFIX]

        # Construct suffix
        output[SUFFIX] = random.randint(0, 1000)
        # Ensure that the numbers in each is different
        while output[SUFFIX] == output[PREFIX]:
            output[SUFFIX] = random.randint(0, 1000)
        task = TASK_TEMPLATE.format(random_number=output[SUFFIX])
        instrs[SUFFIX] = task + " " + instrs[SUFFIX]

        full_prompt = instrs[PREFIX] + '\n' + instrs[SUFFIX]

        testcases.loc[i, 'full_prompt'] = full_prompt
        testcases.loc[i, 'task_1'] = instrs[upper_instr]
        testcases.loc[i, 'task_2'] = instrs[lower_instr]
        testcases.loc[i, 'output_1'] = str(output[upper_instr])
        testcases.loc[i, 'output_2'] = str(output[lower_instr])
        logger.debug(f'gen_testcase: Generated Full Prompt: {full_prompt}')
    logger.info(f"gen_testcase: Generated format capitalization test case")
    return testcases
