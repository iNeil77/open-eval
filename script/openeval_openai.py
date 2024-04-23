import os
import openai
from openai import OpenAI
import termcolor
import jsonlines
import sys

from cdifflib import CSequenceMatcher
from camel_converter import to_snake
# from datasets import load_dataset
from typing import List
from tqdm import tqdm
import argparse
client = OpenAI()

_CITATION = """

}
"""

EOS = ["\ndef", "\nclass ", "\nimport ", "\nfrom ", "\nassert ", "\n# "]

def get_prompt_base(doc):
    return "Complete the following function:\n" + doc["prompt"]

def get_prompt_instruct(doc):
    return doc["instruction"]

def stop_at_stop_token(decoded_string, stop_tokens):
        """
        Produces the prefix of decoded_string that ends at the first occurrence of
        a stop_token.
        WARNING: the decoded_string *must not* include the prompt, which may have stop tokens
        itself.
        """
        min_stop_index = len(decoded_string)
        for stop_token in stop_tokens:
            stop_index = decoded_string.find(stop_token)
            if stop_index != -1 and stop_index < min_stop_index:
                min_stop_index = stop_index
        return decoded_string[:min_stop_index]

class ParseError(Exception):
    pass

class ContentParser:

    @staticmethod
    def _entry_point_variations(entry_point: str) -> List[str]:
        # NOTE: workaround dataset's bug with entry point naming
        return [
            entry_point,
            to_snake(entry_point),
            entry_point[0].lower() + entry_point[1:],
        ]

    def __call__(self, prompt: str, content: str, entry_point: str):
        # NOTE: Model doesn't follow instructions directly:
        # adds description of change and sometimes fixes
        # typos, or other "bugs" in description.
        if "### Response:\n" in content:
            content = content.split("### Response:\n")[1]
        elif "\nassistant\n" in content:
            content = content.split("\nassistant\n")[1]    
        if "```" in content:
            content = content.split("```")[1]
        # first parse with assumption that content has description
        matcher = CSequenceMatcher(None, prompt, content)
        tag, _, _, j1, j2 = matcher.get_opcodes()[-1]
        if tag == "insert":
            return stop_at_stop_token(content[j1:j2], EOS)
        # second parse content with assumption that model wrote code without description
        for entry_point in self._entry_point_variations(entry_point):
            if "def " + entry_point in content:                
                content = content.split(entry_point)[1]
                return stop_at_stop_token("".join(content.splitlines(keepends=True)[1:]), EOS)
        return stop_at_stop_token("".join(content.splitlines(keepends=True)[1:]), EOS)


class ChatWrapper:

    def __init__(self, model: str):
        self._model = model

    def __call__(self, prompt: str, n: int) -> str:
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        # while True:
        # try:
        response = client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0,
            top_p=0.95,
            n=n
        )
        content_list = list()
        for i in range(n):
            message = response.choices[i].message
            assert message.role == "assistant"
            content_list.append(message.content)
        return content_list
        # except Exception as e:
        #     print("API EXCEPTION:", e)


if __name__ == '__main__':
    input_file = "data/open-eval.jsonl"
    args = argparse.ArgumentParser()
    args.add_argument("--times", type=int, default=1)
    args.add_argument("--verbose", type=bool, default=True)
    args.add_argument("--temperature", type=int, default=0)
    args.add_argument("--mode", type=str, default="base")
    args.add_argument("--model", type=str, default="gpt-4-turbo-2024-04-09")
    
    args = args.parse_args()
    TIMES = args.times
    VERBOSE = args.verbose
    TEMPERATURE = args.temperature
    MODE = args.mode
    MODEL = args.model

    samples = []
    with jsonlines.open(input_file) as f:
        for s in f:
            samples.append(s)

    chat_wrapper = ChatWrapper(MODEL)
    parse_errors = 0
    parser = ContentParser()
    for idx, sample in enumerate(tqdm(samples)):
        if MODE == "base":
            prompt = get_prompt_base(sample)
        elif MODE == "instruct":
            prompt = get_prompt_instruct(sample)
        else:
            raise ValueError("Invalid mode")
        
        if VERBOSE:
            print(f"Processing {sample['task_id']} ({idx + 1}/{len(samples)}))...")
        sample["raw_generation"] = chat_wrapper(prompt, TIMES)
        try:
            sample["generation"] = [parser(prompt, generation_item, sample["task_id"]) for generation_item in sample["raw_generation"]]
        except ParseError as e:
            parse_errors += 1
            print("PARSE EXCEPTION:", e)
            sample["generation"] = [""]
        if VERBOSE:
            for i in range(TIMES):
                print(termcolor.colored(sample["task_id"], "yellow", attrs=["bold"]))
                print(termcolor.colored(prompt, "yellow"))
                print(termcolor.colored(sample["canonical_solution"], "red"))
                print(termcolor.colored(sample["generation"][i], "green")+"\n\n")
    if VERBOSE:
        print("parse error rate:", parse_errors / len(samples))

    results_filename = MODEL+f"_{MODE}_completions_"+input_file.split("/")[-1].split(".")[0]+".jsonl"
    with jsonlines.open("results/"+results_filename, "w") as writer:
        writer.write_all(samples)
