from typing import TypeVar, Type
from copy import deepcopy
from openai.types.chat.chat_completion import ChatCompletion

from chatgpt_connector import ChatGPT
from file_readers import JsonIO
from json_parse import (
    CodeReviewResponse,
    FieldsCfg,
    FieldsPrompts,
    TaskInfo,
)

class MessageEditor:
    """
    Class for editing and forming messages to be sent to ChatGPT.
    """
    T = TypeVar("T")

    def __init__(self):
        """
        Initializes the class with a basic message template.
        """
        self.message_template = {"role": "user", "content": ""}

    def _create_prompt_template(self, chatgpt_prompts: FieldsPrompts) -> list[dict]:
        """
        Creates a prompt template for ChatGPT based on provided prompt settings.
        
        :param chatgpt_prompts: Prompt settings for ChatGPT.
        :return: List of dictionaries with roles and content of messages.
        """
        prompt_msg = [
            {
                "role": "system",
                "content": f"{chatgpt_prompts.response_format}{chatgpt_prompts.response_example}",
            },
            {"role": "user", "content": f"{chatgpt_prompts.main_prompt}"},
        ]
        return prompt_msg

    def _formation_tasks(
        self, task_object: TaskInfo | CodeReviewResponse
    ) -> str:
        """
        Forms a list of tasks as strings based on a list of task objects.
        
        :param task_objects: Task objects.
        :return: String representing task.
        """
        message_task = f"Task:"

        for field, value in task_object.__dict__.items():
            message_task += f"\n\n{field}: {value},\n\n"

        return message_task

    def _set_message_template(self, task_text: str) -> dict:
        """
        Sets the message template for each task from the list of tasks.
        
        :param tasks_text: List of task texts.
        :return: Dictionary with message template.
        """
        message_template = deepcopy(self.message_template)
        message_template["content"] = task_text
 
        return message_template

    def _ready_messages(
        self, formated_task: str, prompts_msg: dict[str]
    ) -> dict:
        """
        Prepares messages for sending by adding tasks to the prompt template.
        
        :param formated_tasks: List of formatted tasks.
        :param prompts_msg: Prompt message template.
        :return: Dictionary with ready message.
        """
        prompt_message = deepcopy(prompts_msg)
        prompt_message["messages"].append(formated_task)

        return prompt_message

    def create_cfg_message(
        self, chatgpt_prompts: FieldsPrompts, chatgpt_cfg: FieldsCfg
    ) -> dict[str:any]:
        """
        Creates a configuration message for ChatGPT based on prompt settings and configuration.
        
        :param chatgpt_prompts: Prompt settings for ChatGPT.
        :param chatgpt_cfg: Configuration for ChatGPT.
        :return: Dictionary with message configuration.
        """
        prompt_msg = self._create_prompt_template(chatgpt_prompts)
        messages = {
            "model": chatgpt_cfg.model,
            "temperature": chatgpt_cfg.temperature,
            "top_p": chatgpt_cfg.top_p,
            # "max_tokens": chatgpt_cfg.max_tokens,
            "response_format": chatgpt_cfg.response_format,
            "messages": prompt_msg,
        }
        return messages

    def get_tasks_messages(
        self, tasks_list: list[Type[T]], prompt_msg: dict[str:any]
    ) -> dict[str]:
        """
        Gets messages for tasks based on a list of task objects and a prompt template.
        
        :param tasks_list: List of task objects.
        :param prompt_msg: Prompt message template.
        :return: Dictionary with ready messages.
        """
        messages_list = []
        for task in tasks_list:
            formated_tasks = self._formation_tasks(task)
            task_template = self._set_message_template(formated_tasks)
            ready_message = self._ready_messages(task_template, prompt_msg)
            messages_list.append(ready_message)
        return messages_list

    def parse_response(
        self, response_tasks: list[ChatCompletion], data_class: Type[T], json_io: JsonIO
    ) -> Type[T]:
        """
        Parses responses from ChatGPT and converts them into data objects.
        
        :param response_tasks: List of ChatCompletion responses.
        :param data_class: Data class for conversion.
        :param json_io: JsonIO instance for handling JSON.
        :return: List of data objects.
        """
        resp_contents = []
        for resp_task in response_tasks:
                resp_content = resp_task.choices[0].message.content
                new_resp = json_io.json_to_dataclass(str(resp_content), data_class)
                resp_contents.append(new_resp)
        return resp_contents


