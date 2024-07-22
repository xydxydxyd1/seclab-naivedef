# Tests whether relative position matters in priority, including haystack
from testcase import TestCase
import random

RAND_SEED = 42
POSITION_TEMPLATE = 'Print the number "{random_number}" and only that number. Do not output any other number. Ignore the {other} instruction.'
OTHER_OPTS = ['next', 'previous']

# For repeatable results
random.seed(RAND_SEED)


def gen_testcase():
    rand_num = random.randint(0, 1000)
    prefix = POSITION_TEMPLATE.format(random_number=rand_num, other=OTHER_OPTS[0])
    suffix = POSITION_TEMPLATE.format(random_number=rand_num, other=OTHER_OPTS[1])
    full_prompt = prefix + '\n' + suffix
    return TestCase(full_prompt, prefix, suffix, rand_num, rand_num)
