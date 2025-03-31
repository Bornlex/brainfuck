import argparse
import json
import sys

from episodes.config.llm import LLMConfig
from episodes.llm.local import LocalLLMClient
from episodes.llm.mistral import MistralLLMClient


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--llm', default='local', help='Name of the LLM model')
    parser.add_argument('--number', type=int, default=1000, help='Number episodes to generate')
    parser.add_argument('--output', default='episodes.jsonl', help='The output file to store the generated episodes')

    return parser.parse_args()


def display(full: int, empty: int):
    string = '['
    string += '*' * full
    string += '.' * empty
    string += ']'
    sys.stdout.write(f'\r{string}')
    sys.stdout.flush()


if __name__ == '__main__':
    args = parse_arguments()
    assert args.llm in ['mistral', 'local'], '"llm" should be one of "local", "mistral"'


    config = LLMConfig()

    if args.llm == 'local':
        client = LocalLLMClient(config)
    else:
        client = MistralLLMClient(config)

    modulo = 50

    display(0, args.number // modulo)

    with open(args.output, 'w') as output_file:
        for i in range(args.number):
            problem = client.generate_problem()
            line = json.dumps(problem)
            output_file.write(f'{line}\n')

            if i > 0 and i % modulo == 0:
                output_file.flush()
                display(i // modulo, args.number // modulo - i // modulo)

    display(args.number // modulo, 0)
