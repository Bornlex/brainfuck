import json
from mistralai import Mistral

from episodes.config.llm import LLMConfig
from episodes.llm.client import LLMClient


class MistralLLMClient(LLMClient):
    def __init__(self, llm_config: LLMConfig):
        super().__init__(llm_config)

        self.__client = Mistral(api_key=self.__config.API_KEY)

    def completion(self, messages: list, retry: int = 3) -> str | None:
        while retry > 0:
            response = self.__do_request(messages)

            try:
                answer = json.loads(response)["content"]
                return answer
            except (json.JSONDecodeError, KeyError):
                retry -= 1

        return None

    def __do_request(self, messages: list) -> str | None:
        response = self.__client.chat.complete(
            model=self.__config.MODEL,
            messages=messages
        )

        return response.choices[0].message.content
