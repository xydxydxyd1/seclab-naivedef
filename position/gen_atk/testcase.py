# Definition for a test case class

class TestCase:
    def __init__(self, full_prompt, task_1, task_2, output_1, output_2):
        self.full_prompt = full_prompt
        self.task_1 = task_1
        self.task_2 = task_2
        self.output_1 = output_1
        self.output_2 = output_2
    def __str__(self):
        return f"Prompt:\n{self.full_prompt}\n\nTask 1:\n{self.task_1}\n\nIntended output 1:\n{self.output_1}\n\nTask 2:\n{self.task_2}\n\nIntended output 2:\n{self.output_2}"