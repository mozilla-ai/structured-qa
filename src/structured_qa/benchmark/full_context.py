import re

import PyPDF2
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


def load_pdf(pdf_file: str) -> str | None:
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        return "\n".join(page.extract_text() for page in pdf_reader.pages)
    except Exception as e:
        logger.exception(e)
        return None


def clean_with_regex(text: str) -> str:
    text = re.sub(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        "",
        text,
    )
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.[\w]+", "", text)
    text = re.sub(r'[^a-zA-Z0-9\s.,!?;:"\']', "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def full_context_process_document(
    document_file,
    document_data,
    model,
    answer_prompt: str = ANSWER_WITH_TYPE_PROMPT,
):
    document = clean_with_regex(load_pdf(document_file))

    max_characters = model.n_ctx() * 4
    if len(document) > max_characters:
        logger.warning(
            f"Input text is too big ({len(document)})."
            f" Using only a subset of it ({max_characters})."
        )
    document = document[:max_characters]

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
        except Exception as e:
            logger.exception(e)
            logger.error("Failed to generate completion")
            response = "Generation Error"
        answers[index] = response
        sections[index] = None

    return answers, sections
