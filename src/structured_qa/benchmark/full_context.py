import pymupdf4llm
from loguru import logger


ANSWER_WITH_TYPE_PROMPT = """
You are a rigorous assistant answering questions.
You only answer based on the current information available.
You should only answer with ANSWER_TYPE.

The current information available is:

```
{CURRENT_INFO}
```
"""


def full_context_process_document(
    document_file,
    document_data,
    model,
    answer_prompt: str = ANSWER_WITH_TYPE_PROMPT,
):
    md_text = pymupdf4llm.to_markdown(document_file)

    logger.info("Predicting")
    answers = {}
    sections = {}
    for index, row in document_data.iterrows():
        question = row["question"]
        try:
            float(row["answer"])
            answer_type = "a number"
        except ValueError:
            if row["answer"] in ("YES", "NO"):
                answer_type = "YES or NO"
            else:
                answer_type = "a single letter"

            answer_prompt = answer_prompt.replace("ANSWER_TYPE", answer_type)

        logger.info(f"Question: {question}")
        messages = [
            {
                "role": "system",
                "content": answer_prompt.format(CURRENT_INFO="\n".join(md_text)),
            },
            {"role": "user", "content": question},
        ]
        try:
            response = model.get_response(messages)
        except Exception as e:
            logger.exception(e)
            logger.error("Failed to generate completion")
            return "Generation Error", [None]
        answers[index] = response
        sections[index] = None

    return answers, sections
