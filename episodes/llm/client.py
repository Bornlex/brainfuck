from abc import abstractmethod, ABC

from episodes.config.llm import LLMConfig
from episodes.llm import prompt


class LLMClient(ABC):
    def __init__(self, llm_config: LLMConfig):
        self.__config = llm_config

    @property
    def config(self):
        return self.__config

    @abstractmethod
    def completion(self, messages: list[dict], retry: int = 3) -> str | None:
        pass

    def generate_problem(self) -> str | None:
        system_prompt = LLMClient.__format_prompt(
            prompt.prompt,
            prompt.examples
        )
        messages = [{
            'role': 'system',
            'content': system_prompt
        }, {
            'role': 'user',
            'content': f'Generate a new problem.'
        }]

        return self.completion(messages)

    @staticmethod
    def __format_prompt(system_prompt: str, examples: list[str]) -> str:
        if examples:
            examples = [f'- {example}' for example in examples]
            examples_string = '\n'.join(examples)

            return f'{system_prompt}\nHere are some examples:\n{examples_string}.'

        return system_prompt
