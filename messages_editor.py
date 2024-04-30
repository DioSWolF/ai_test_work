from typing import TypeVar, Type
from copy import deepcopy
from chatgpt_connevtor import ChatGPT
from file_readers import JsonIO

from json_parse import ChatGPTPrompts, CodeReviewResponse, FieldsCfg, TaskInfo


class MessageEditor:
    T = TypeVar("T")

    def __init__(self, chatgpt_prompts: ChatGPTPrompts):
        """
        Initializes the MessageEditor class.
        :param chatgpt_prompts: ChatGPTPrompts object.
        """
        self.message_template = {"role": "user", "content": ""}
        self.code_review_prompt_msg = [
            {
                "role": "system",
                "content": f"{chatgpt_prompts.code_review.response_format}{chatgpt_prompts.code_review.response_example}",
            },
            {"role": "user", "content": f"{chatgpt_prompts.code_review.main_prompt}"},
        ]
        self.friendly_prompt_msg = [
            {
                "role": "system",
                "content": f"{chatgpt_prompts.code_review.response_format}",
            },
            {
                "role": "user",
                "content": f"{chatgpt_prompts.friendly_format.main_prompt}",
            },
        ]

    def _formation_tasks(
        self, task_objects: list[TaskInfo | CodeReviewResponse]
    ) -> list[str]:
        """
        Forms a list of tasks.
        :param task_objects: List of task objects.
        :return: List of tasks as strings.
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
        Sets the message template.
        :param tasks_text: List of tasks as strings.
        :return: List of messages.
        """
        message_template = deepcopy(self.message_template)
        message_list = []

        for task_text in tasks_text:
            message_template["content"] = task_text
            message_list.append(message_template.copy())

        return message_list

    def _convert_response(
        self, resp_content: list[str], data_class: Type[T], json_io: JsonIO
    ) -> list[Type[T]]:
        """
        Converts the response.
        :param resp_content: List of responses as strings.
        :param data_class: Data class.
        :param json_io: JsonIO object.
        :return: List of responses as data class objects.
        """
        dataclasses_list = []

        for json_resp in resp_content:
            new_resp = json_io.json_to_dataclass(str(json_resp), data_class)
            dataclasses_list.append(new_resp)

        return dataclasses_list

    def get_tasks_messages(self, tasks_list: list[Type[T]]) -> list[dict[str:str]]:
        """
        Gets messages for tasks.
        :param tasks_list: List of tasks.
        :return: List of messages for tasks.
        """
        tasks = self._formation_tasks(tasks_list)
        formated_tasks = self._set_message_template(tasks)
        return formated_tasks

    def create_message_data(
        self, message: list[dict], chatgpt_cfg: FieldsCfg
    ) -> dict[str:any]:
        """
        Creates data for the message.
        :param message: List of messages.
        :param chatgpt_cfg: ChatGPT configuration.
        :return: Data for the message.
        """
        messages = {
            "model": chatgpt_cfg.model,
            "temperature": chatgpt_cfg.temperature,
            "top_p": chatgpt_cfg.top_p,
            # "max_tokens": chatgpt_cfg.max_tokens,
            "response_format": chatgpt_cfg.response_format,
            "messages": message,
        }
        return messages

    async def request_response_chatgpt(
        self,
        formated_tasks: list[str],
        prompts_msg: dict[str:str],
        data_class: Type[T],
        chatgpt: ChatGPT,
        json_io: JsonIO,
    ) -> list[Type[T]]:
        """
        Requests a response from ChatGPT.
        :param formated_tasks: List of formatted tasks.
        :param prompts_msg: Messages for tasks.
        :param data_class: Data class.
        :param chatgpt: ChatGPT object.
        :param json_io: JsonIO object.
        :return: List of responses as data class objects.
        """
        resp_content = []

        for task in formated_tasks:
            prompt_message = deepcopy(prompts_msg)
            prompt_message["messages"].append(task)

            resp_tasks = await chatgpt.send_request(prompt_message)
            resp_content.append(resp_tasks.choices[0].message.content)

        return self._convert_response(resp_content, data_class, json_io)
