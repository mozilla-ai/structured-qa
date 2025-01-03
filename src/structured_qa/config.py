from typing_extensions import Annotated

from pydantic import BaseModel, DirectoryPath, FilePath
from pydantic.functional_validators import AfterValidator


def validate_model(value):
    parts = value.split("/")
    if len(parts) != 3:
        raise ValueError("model must be formatted as `owner/repo/file`")
    if not value.endswith(".gguf"):
        raise ValueError("model must be a gguf file")
    return value


def validate_find_prompt(value):
    if "{SECTIONS}" not in value:
        raise ValueError("find_prompt must contain `{SECTIONS}` placeholder")
    return value


def answer_prompt(value):
    if "{CURRENT_INFO}" not in value:
        raise ValueError("answer_prompt must contain `{CURRENT_INFO}` placeholder")
    return value


class Config(BaseModel):
    input_file: FilePath
    output_dir: DirectoryPath
    model: Annotated[str, AfterValidator(validate_model)]
    answer_prompt: Annotated[str, AfterValidator(answer_prompt)]
    find_prompt: Annotated[str, AfterValidator(validate_find_prompt)]
