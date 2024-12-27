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


class Config(BaseModel):
    input_file: FilePath
    output_dir: DirectoryPath
    model: Annotated[str, AfterValidator(validate_model)]
