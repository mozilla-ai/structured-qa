import re
from pathlib import Path


from llama_cpp import Llama
from loguru import logger


FIND_PROMPT = """
Given an input question, you need to pick a `section_name` from the following list
based on how related the name is to the question:

```
{SECTIONS}
```

You will return the `section_name` and no additional text.
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

"""
org, repo, filename = model_id.split("/")
model = Llama.from_pretrained(
    repo_id=f"{org}/{repo}",
    filename=filename,
    n_ctx=0,
    verbose=False
)
"""
def find_retrieve_answer(
    model: Llama, 
    sections_dir: str, 
    question: str,
    find_prompt: str = FIND_PROMPT,
    answer_prompt: str = ANSWER_PROMPT
) -> tuple[str, list[str]] | tuple[None, list[str]]:
    sections_dir = Path(sections_dir)
    sections_names = [
        section.stem for section in sections_dir.glob("*.txt")
    ]
    current_info = None
    current_section = None

    sections_checked = []
    while True:
        logger.debug(f"Current information available: {current_info}")
        if not current_info:
            logger.debug("Finding section")
            finding_section = True
            messages = [
                { "role": "system", "content": find_prompt.format(
                    SECTIONS="\n".join(sections_names)) 
                },
                { "role": "user", "content": question},
            ]
        else:
            logger.debug("Answering question")
            finding_section = False
            messages = [
                { "role": "system", "content": answer_prompt.format(
                    CURRENT_INFO=current_info) 
                },
                { "role": "user", "content": question},
            ]

        result = model.create_chat_completion(messages)
        result = result["choices"][0]["message"]["content"]

        logger.debug(f"Result: {result}")

        if finding_section:
            result = result.strip()
            logger.info(f"Retrieving section: {result}")
            if result in sections_names:
                section_content = (
                    sections_dir / f"{result}.txt"
                ).read_text()
                current_section = result
                current_info = section_content
                sections_checked.append(result)
            else:
                logger.error(f"Unknown section: {result}")
                return None, sections_checked
        else:
            if result == "I need more info.":
                current_info = None
                sections_names.remove(current_section)
                continue
            else:
                return result, sections_checked
