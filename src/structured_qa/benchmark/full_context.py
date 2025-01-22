from pathlib import Path
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


def fra_process_document(
    document_file,
    document_data,
    model,
    answer_prompt: str = ANSWER_WITH_TYPE_PROMPT,
):
    document = Path(document_file).read_text().strip()

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
                "content": answer_prompt.format(CURRENT_INFO="\n".join(document)),
            },
            {"role": "user", "content": question},
        ]
        try:
            response = model.get_response(messages)
        except Exception:
            logger.error("Failed to generate completion")
            return "Generation Error", []
        answers[index] = response
        sections[index] = None

    return answers, sections
