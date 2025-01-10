from pathlib import Path


from llama_cpp import Llama
from loguru import logger


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


def find_retrieve_answer(
    model: Llama,
    sections_dir: str,
    question: str,
    find_prompt: str = FIND_PROMPT,
    answer_prompt: str = ANSWER_PROMPT,
) -> tuple[str, list[str]] | tuple[None, list[str]]:
    sections_dir = Path(sections_dir)
    sections_names = [section.stem for section in sections_dir.glob("*.txt")]
    current_info = None
    current_section = None

    sections_checked = []
    while True:
        logger.debug(f"Current information available: {current_info}")
        if not current_info:
            logger.debug("Finding section")
            finding_section = True
            messages = [
                {
                    "role": "system",
                    "content": find_prompt.format(SECTIONS="\n".join(sections_names)),
                },
                {"role": "user", "content": question},
            ]
        else:
            logger.debug("Answering question")
            finding_section = False
            messages = [
                {
                    "role": "system",
                    "content": answer_prompt.format(CURRENT_INFO=current_info),
                },
                {"role": "user", "content": question},
            ]

        result = model.create_chat_completion(messages)
        result = result["choices"][0]["message"]["content"]

        logger.debug(f"Result: {result}")

        if finding_section:
            result = result.strip()
            logger.info(f"Retrieving section: {result}")
            if result in sections_names:
                section_content = (sections_dir / f"{result}.txt").read_text()
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
