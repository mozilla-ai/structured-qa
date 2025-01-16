from typing_extensions import Annotated

from pydantic import BaseModel, DirectoryPath, FilePath
from pydantic.functional_validators import AfterValidator


FIND_PROMPT = """
You are given two pieces of information:
1. A user question.
2. A list of valid section names.

Your task is to:
- Identify exactly one `section_name` from the provided list that seems related to the user question.
- Return the `section_name` exactly as it appears in the list.
- Do NOT return any additional text, explanation, or formatting.
- Do NOT combine multiple section names into a single response.

Here is the list of valid `section_names`:

```
{SECTIONS}
```

Now, based on the input question, return the single most relevant `section_name` from the list.
"""

ANSWER_PROMPT = """
You are a rigorous assistant answering questions.
You only answer based on the current information available.

The current information available is:

```
{CURRENT_INFO}
```

If the current information available not enough to answer the question,
you must return the following message and nothing else:

```
I need more info.
```
"""


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
