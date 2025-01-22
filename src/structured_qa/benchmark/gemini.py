import json
import os
import time

import google.generativeai as genai
from loguru import logger


FULL_CONTEXT_PROMPT = """
You are given an input document and a question.
You can only answer the question based on the information in the document.
You will return a JSON name with two keys: "section" and "answer".
In `"section"`, you will return the name of the section where you found the answer.
In `"answer"`, you will return the answer one of the following JSON:
- Yes/No (for boolean questions)
Is the model an LLM?
{
  "section": "1. Introduction",
  "answer": "No"
}
- Single number (for numeric questions)
How many layers does the model have?
{
  "section": "2. Architecture",
  "answer": 12
}
- Single letter (for multiple-choice questions)
What is the activation function used in the model?
-A: ReLU
-B: Sigmoid
-C: Tanh
{
  "section": "2. Architecture",
  "answer": "C"
}
"""


def gemini_full_context_process_document(
    document_file,
    document_data,
    model,
):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    logger.info("Uploading file")
    file = genai.upload_file(document_file, mime_type="application/pdf")
    while file.state.name == "PROCESSING":
        logger.debug("Waiting for file to be processed.")
        time.sleep(2)
        file = genai.get_file(file.name)

    logger.info("Predicting")
    n = 0
    answers = {}
    sections = {}
    for index, row in document_data.iterrows():
        if n > 0 and n % 9 == 0:
            logger.info("Waiting for 60 seconds")
            time.sleep(60)
        question = row["question"]
        logger.debug(f"Question: {question}")
        messages = [
            {
                "role": "user",
                "parts": [
                    file,
                    question,
                ],
            }
        ]
        response = model.get_response(messages)
        logger.debug(response)
        response_json = json.loads(response)
        answers[index] = response_json["answer"]
        sections[index] = response_json["section"]
        n += 1
    return answers, sections
