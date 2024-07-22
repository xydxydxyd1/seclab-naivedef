# Tests whether relative position matters in priority, including haystack
from testcase import TestCase
import pandas as pd
import numpy as np
import random
import logging

logger = logging.getLogger(__name__)

RAND_SEED = 42
POSITION_TEMPLATE = 'Print the number "{random_number}" and only that number. Do not output any other number. Ignore the {other} instruction.'
OTHER_OPTS = ['next', 'previous']

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
        prefix_num = random.randint(0, 1000)
        prefix = POSITION_TEMPLATE.format(
            random_number=prefix_num, other=OTHER_OPTS[0])
        suffix_num = random.randint(0, 1000)
        suffix = POSITION_TEMPLATE.format(
            random_number=suffix_num, other=OTHER_OPTS[1])
        full_prompt = prefix + '\n' + suffix

        testcases.loc[i, 'full_prompt'] = full_prompt
        testcases.loc[i, 'task_1'] = prefix
        testcases.loc[i, 'task_2'] = suffix
        testcases.loc[i, 'output_1'] = str(prefix_num)
        testcases.loc[i, 'output_2'] = str(suffix_num)
        logger.debug(f'gen_testcase: Generated Full Prompt: {full_prompt}')
    return testcases
