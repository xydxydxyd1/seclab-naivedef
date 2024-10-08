# Interface for a test object, which defines methods for generating tests and
# judging a test given a result
from abc import ABC, abstractmethod
import pandas as pd


class Test(ABC):

    @property
    @abstractmethod
    def seed(self) -> int:
        """The seed used to generate the random test cases"""
        pass

    @seed.setter
    @abstractmethod
    def seed(self, value):
        pass

    @abstractmethod
    def gen_tests(self, num_tests):
        """Generate a number of tests."""
        pass

    @abstractmethod
    def tests(self) -> pd.DataFrame:
        """The list of generated tests in a dataframe, including column
        `full_prompt` that is the input to a language model, `task_{1|2}`,
        `output_{1|2}` that is the task and output of each instruction"""
        pass
