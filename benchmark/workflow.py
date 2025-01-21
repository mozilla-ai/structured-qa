from loguru import logger

from structured_qa.config import FIND_PROMPT
from structured_qa.model_loaders import load_llama_cpp_model
from structured_qa.preprocessing import document_to_sections_dir
from structured_qa.workflow import find_retrieve_answer


ANSWER_WITH_TYPE_PROMPT = """
You are a rigorous assistant answering questions.
You only answer based on the current information available.
You should only answer with ANSWER_TYPE.

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


def workflow_process_document(
    document_file,
    document_data,
    model_id: str = "bartowski/Qwen2.5-7B-Instruct-GGUF/Qwen2.5-7B-Instruct-Q8_0.gguf",
    find_prompt: str = FIND_PROMPT,
    answer_prompt: str = ANSWER_WITH_TYPE_PROMPT,
):
    logger.info("Creating model")
    model = load_llama_cpp_model(model_id)

    logger.info("Splitting document into sections")
    sections_dir = "sections"
    document_to_sections_dir(document_file, sections_dir)

    logger.info("Predicting")
    answers = {}
    sections = {}
    for index, row in document_data.iterrows():
        question = row["question"]
        try:
            float(row["answer"])
            answer_type = "a single number"
        except ValueError:
            if row["answer"] in ("YES", "NO"):
                answer_type = "YES or NO"
            else:
                answer_type = "a single letter"

            answer_prompt = answer_prompt.replace("ANSWER_TYPE", answer_type)

        logger.info(f"Question: {question}")
        answer, sections_checked = find_retrieve_answer(
            question, model, sections_dir, find_prompt, answer_prompt
        )

        answers[index] = answer
        sections[index] = sections_checked[-1] if sections_checked else None

    return answers, sections
