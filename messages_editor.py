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
        self, task_objects: list[TaskInfo | CodeReviewResponse]
    ) -> list[str]:
        """
        Forms a list of tasks as strings based on a list of task objects.
        
        :param task_objects: List of task objects.
        :return: List of strings representing tasks.
        """
        tasks_list = []
        i = 1

        for task in task_objects:
            message_task = f"Task {i}:"

            for field, value in task.__dict__.items():
                message_task += f"\n\n{field}: {value},\n\n"

            tasks_list.append(message_task)
            message_task = ""
            i += 1

        return tasks_list

    def _set_message_template(self, tasks_text: list[str]) -> list[dict]:
        """
        Sets the message template for each task from the list of tasks.
        
        :param tasks_text: List of task texts.
        :return: List of dictionaries with message templates.
        """
        message_template = deepcopy(self.message_template)
        message_list = []

        for task_text in tasks_text:
            message_template["content"] = task_text
            message_list.append(message_template.copy())

        return message_list

    def _ready_messages(
        self, formated_tasks: list[str], prompts_msg: dict[str]
    ) -> list[dict]:
        """
        Prepares messages for sending by adding tasks to the prompt template.
        
        :param formated_tasks: List of formatted tasks.
        :param prompts_msg: Prompt message template.
        :return: List of dictionaries with ready messages.
        """
        ready_tasks = []
        for task in formated_tasks:
            prompt_message = deepcopy(prompts_msg)
            prompt_message["messages"].append(task)
            ready_tasks.append(prompt_message)
        return ready_tasks

    def _convert_response(
        self, resp_content: list[str], data_class: Type[T], json_io: JsonIO
    ) -> list[Type[T]]:
        """
        Converts responses from JSON to data objects.
        
        :param resp_content: List of JSON response strings.
        :param data_class: Data class for conversion.
        :param json_io: JsonIO instance for handling JSON.
        :return: List of data objects.
        """
        dataclasses_list = []

        for json_resp in resp_content:
            new_resp = json_io.json_to_dataclass(str(json_resp), data_class)
            dataclasses_list.append(new_resp)

        return dataclasses_list

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
        tasks = self._formation_tasks(tasks_list)
        formated_tasks = self._set_message_template(tasks)
        ready_messages = self._ready_messages(formated_tasks, prompt_msg)
        return ready_messages

    def parse_response(
        self, response_tasks: list[ChatCompletion], data_class: Type[T], json_io: JsonIO
    ):
        """
        Parses responses from ChatGPT and converts them into data objects.
        
        :param response_tasks: List of ChatCompletion responses.
        :param data_class: Data class for conversion.
        :param json_io: JsonIO instance for handling JSON.
        :return: List of data objects.
        """
        resp_content = []
        for resp_tasks in response_tasks:
            resp_content.append(resp_tasks.choices[0].message.content)
        return self._convert_response(resp_content, data_class, json_io)
