from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion


class ChatGPT:
    """
    Class for working with the OpenAI ChatGPT API.
    """

    def __init__(self, api_key: str) -> ChatCompletion:
        """
        Class initialization.
        :param api_key: API key for AsyncOpenAI/OpenAI .
        """
        self.openai = AsyncOpenAI(api_key=api_key)

    async def send_request(self, request_data: dict):
        """
        Send a request to the OpenAI ChatGPT API.
        :param request_data: Request data.
        :return: API response.
        """
        self.response = await self.openai.chat.completions.create(**request_data)
        return self.response
