# API method wrappers for ChatGPT
import time
import numpy as np
import logging
import os
from dotenv import load_dotenv
from openai import OpenAI

logger = logging.getLogger(__name__)
load_dotenv()
client = OpenAI(organization=os.environ.get("OPENAI_ORG_ID"))


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
