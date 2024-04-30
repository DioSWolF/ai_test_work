import json
import os
from typing import Type, TypeVar
from dacite import from_dict
from dotenv import load_dotenv


class JsonIO:
    """
    Class for working with JSON files.
    """

    T = TypeVar("T")

    def __init__(self):
        self.json = json

    def get_json_data(self, file_path: str, data_class: Type[T]) -> Type[T]:
        """
        Get data from a JSON file.
        :param file_path: Path to the JSON file.
        :param data_class: The class to which the data should be converted.
        :return: Data as an instance of the data_class class.
        """
        with open(file_path, "r") as file:
            data = self.json.load(file)
        return from_dict(data_class=data_class, data=data)

    def save_json_data(self, file_path: str, data: dict):
        """
        Save data to a JSON file.
        :param file_path: Path to the JSON file.
        :param data: Data to be saved.
        """
        with open(file_path, "w") as file:
            self.json.dump(data, file)

    def json_to_dataclass(self, dict_str: str, data_class: Type[T]) -> Type[T]:
        """
        Convert a JSON string to an instance of a class.
        :param dict_str: JSON string.
        :param data_class: The class to which the data should be converted.
        :return: Data as an instance of the data_class class.
        """
        data = self.json.loads(dict_str)
        return from_dict(data_class=data_class, data=data)


class EnvReader:
    """
    Class for reading environment variables.
    """

    def __init__(self, file_path: str):
        """
        Class initialization.
        :param file_path: Path to the file with environment variables.
        """
        self.file_path = file_path
        self.load_env_vars()

    def load_env_vars(self):
        """
        Load environment variables.
        """
        load_dotenv(self.file_path)
        self.chatgpt_api_key = os.getenv("CHATGPT_API_KEY")
        self.chatgpt_cfg_path = os.getenv("CHATGPT_CFG_PATH")
        self.chatgpt_prompts_path = os.getenv("CHATGPT_PROMPTS_PATH")
        self.python_tasks_path = os.getenv("PYTHON_TASKS_PATH")
