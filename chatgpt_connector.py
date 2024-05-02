import asyncio
from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion


class ChatGPT:
    """
    Class for interacting with the OpenAI ChatGPT API.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes the class using an API key.

        :param api_key: API key for accessing AsyncOpenAI/OpenAI.
        """
        self.openai = AsyncOpenAI(api_key=api_key)

    async def send_request(self, request_data: dict) -> ChatCompletion:
        """
        Sends a request to the OpenAI ChatGPT API.

        :param request_data: Request data in dictionary format.
        :return: Response from the API as a ChatCompletion object.
        """
        self.response = await self.openai.chat.completions.create(**request_data)
        return self.response

    async def async_request_response_chatgpt(
        self,
        ready_tasks: list[dict[str, any]],
    ) -> list[any]:
        """
        Asynchronously sends a list of requests to the API and returns the responses.

        :param ready_tasks: List of tasks in the form of a list of dictionaries.
        :return: List of responses from the API.
        """
        coroutines = [self.send_request(task) for task in ready_tasks]
        response = await asyncio.gather(*coroutines)
        return response
