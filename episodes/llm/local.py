import json
import requests

from episodes.config.llm import LLMConfig
from episodes.llm.client import LLMClient


class LocalLLMClient(LLMClient):
    def __init__(self, llm_config: LLMConfig):
        super().__init__(llm_config)

    def completion(self, messages: list, retry: int = 3) -> str | None:
        while retry > 0:
            response = self.__do_request(messages)

            try:
                answer = json.loads(response)
                return answer
            except (json.JSONDecodeError, KeyError):
                retry -= 1

        return None

    def __do_request(self, messages: list[dict]):
        response = requests.post(
            self.config.URL,
            json={'messages': messages},
            headers={'Authorization': f'Bearer {self.config.API_KEY}'},
        )
        if response.status_code != 200:
            return None

        return response.json()['choices'][0]['message']['content']
