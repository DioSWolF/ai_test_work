import asyncio
from chatgpt_connector import ChatGPT
from file_readers import EnvReader, JsonIO
from json_parse import ChatGPTCfg, ChatGPTPrompts, CodeReviewResponse, PythonCode
from messages_editor import MessageEditor


class StartProgram:

    def __init__(self):
        """
        Initialize the StartProgram class.
        """
        self.json_io = JsonIO()
        self.env_reader = EnvReader(".env")
        self.env_reader.load_env_vars()

        self.chatgpt_cfg = self.json_io.get_json_data(
            self.env_reader.chatgpt_cfg_path, ChatGPTCfg
        )
        self.chatgpt_prompts = self.json_io.get_json_data(
            self.env_reader.chatgpt_prompts_path, ChatGPTPrompts
        )
        self.python_code = self.json_io.get_json_data(
            self.env_reader.python_tasks_path, PythonCode
        )
        self.msg_editor = MessageEditor(self.chatgpt_prompts)
        self.chatgpt = ChatGPT(self.env_reader.chatgpt_api_key)

    async def start(self):
        """
        Start the program.
        """
        await self._review()
        print("\nREVIEW RESPONSE:\n")
        self._print_responses(self.review_response)
        await self._friendly()
        print("\nFRIENDLY RESPONSE:\n")
        self._print_responses(self.friendly_response)

    async def _review(self):
        """
        Review the code.
        """
        self.review_prompt = self.msg_editor.create_message_data(
            self.msg_editor.code_review_prompt_msg,
            chatgpt_cfg=self.chatgpt_cfg.code_review,
        )
        self.review_tasks = self.msg_editor.get_tasks_messages(
            self.python_code.python.code_problems
        )
        self.review_response = await self.msg_editor.request_response_chatgpt(
            self.review_tasks,
            self.review_prompt,
            CodeReviewResponse,
            self.chatgpt,
            self.json_io,
        )

    async def _friendly(self):
        """
        Make the code friendly.
        """
        self.friendly_prompt = self.msg_editor.create_message_data(
            self.msg_editor.friendly_prompt_msg,
            chatgpt_cfg=self.chatgpt_cfg.code_friendly,
        )
        self.friendly_tasks = self.msg_editor.get_tasks_messages(self.review_response)
        self.friendly_response = await self.msg_editor.request_response_chatgpt(
            self.friendly_tasks,
            self.friendly_prompt,
            CodeReviewResponse,
            self.chatgpt,
            self.json_io,
        )

    def _print_responses(self, resp_list: list[CodeReviewResponse]):
        for resp in resp_list:
            print(str(resp))


if __name__ == "__main__":
    a = StartProgram()
    asyncio.run(a.start())
