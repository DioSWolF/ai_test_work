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
        self.msg_editor = MessageEditor()
        self.chatgpt = ChatGPT(self.env_reader.chatgpt_api_key)

    # def start(self):                                                                          #TODO:        Use in vscode, pycharm, etc.
    #     """
    #     Start the program.
    #     """
        # self.review()
        # print("\nREVIEW RESPONSE:\n")
        # self._print_responses(self.review_response)
        # self.friendly()
        # print("\nFRIENDLY RESPONSE:\n")
        # self._print_responses(self.friendly_response)

    async def review(self):                                                                     #TODO:        Use in google notebook, jupiter notebook.
        # def review(self):                                                                     #TODO:        Use in vscode, pycharm, etc.
        """
        Review the code.
        """
        self.review_cfg_prompt = self.msg_editor.create_cfg_message(
            self.chatgpt_prompts.code_review,
            chatgpt_cfg=self.chatgpt_cfg.code_review,
        )
        self.review_tasks = self.msg_editor.get_tasks_messages(
            self.python_code.python.code_problems,
            self.review_cfg_prompt,
        )
        self.response = await self.chatgpt.async_request_response_chatgpt(self.review_tasks)    #TODO:        Use in google notebook, jupiter notebook.

        # self.response = asyncio.run(
        #     self.chatgpt.async_request_response_chatgpt(self.review_tasks)                    #TODO:        Use in vscode, pycharm, etc.
        #     )
        
        self.review_response = self.msg_editor.parse_response(
            self.response, CodeReviewResponse, self.json_io
        )

    async def friendly(self):                                                                   #TODO:        Use in google notebook, jupiter notebook.
        # def friendly(self):                                                                   #TODO:        Use in vscode, pycharm, etc.
        """
        Make the review response friendly.
        """

        self.friendly_cfg_prompt = self.msg_editor.create_cfg_message(
            self.chatgpt_prompts.code_friendly,
            chatgpt_cfg=self.chatgpt_cfg.code_friendly,
        )
        self.friendly_tasks = self.msg_editor.get_tasks_messages(
            self.review_response,
            self.friendly_cfg_prompt,
        )
        self.response = await self.chatgpt.async_request_response_chatgpt(self.friendly_tasks)  #TODO:        Use in google notebook, jupiter notebook.
        
        # self.response = asyncio.run(
        #     self.chatgpt.async_request_response_chatgpt(self.friendly_tasks)                  #TODO:        Use in vscode, pycharm, etc.
        # )
        self.friendly_response = self.msg_editor.parse_response(
            self.response, CodeReviewResponse, self.json_io
        )

    def _print_responses(self, resp_list: list[CodeReviewResponse]):
        for resp in resp_list:
            print(str(resp))


# if __name__ == "__main__":                                                                    #TODO:        Use in vscode, pycharm, etc.
#     a = StartProgram()
#     a.start()
