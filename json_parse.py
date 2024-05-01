from dataclasses import dataclass


# TODO: Classes for json tasks
@dataclass
class TestCases:
    input: str
    output: str


@dataclass
class TaskInfo:
    topic_id: int
    # topic_title: str
    # topic_theory_url: str
    step_id: int
    step_title: str
    step_description: str
    # step_url: str
    test_cases: list[TestCases]
    code_template: str
    wrong_code_submission: str
    # default_feedback: str
    # gpt_current_feedback: str
    correct_code_submission: str


@dataclass
class CodeProblem:
    code_problems: list[TaskInfo]


@dataclass
class PythonCode:
    python: CodeProblem


# TODO: ChatGpt configs
@dataclass
class FieldsCfg:
    temperature: float
    top_p: float
    model: str
    max_tokens: int
    min_tokens: int
    response_format: dict


@dataclass
class ChatGPTCfg:
    code_review: FieldsCfg
    code_friendly: FieldsCfg


# TODO: ChatGPT prompts
@dataclass
class CodeReviewPrompt:
    main_prompt: str
    response_format: str
    response_example: str


@dataclass
class FriendlyPrompt:
    main_prompt: str
    response_example: str


@dataclass
class ChatGPTPrompts:
    code_review: CodeReviewPrompt
    friendly_format: FriendlyPrompt


# TODO: ChatGPT response
@dataclass
class CodeReviewResponse:
    topic_id: int
    step_id: int
    errors: list[str]
    recommendations: list[str]

    def __str__(self) -> str:
        return f'{{\n"topic_id": {self.topic_id},\n"step_id": {self.step_id},\n"errors": {self.errors},\n"recommendations": {self.recommendations},\n}}'
