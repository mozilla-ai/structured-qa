import datetime
import json
import os
import time

import google.generativeai as genai
from loguru import logger

SYSTEM_PROMPT = """
You are given an input document and a question.
You can only answer the question based on the information in the document.
You will return a JSON name with two keys: "section" and "answer".
In `"section"`, you will return the name of the section where you found the answer.
In `"answer"`, you will return the answer either as Yes/No (for boolean questions) or as a single number (for numeric questions).
Example response:
{
  "section": "1. Introduction",
  "answer": "No"
}
"""


def gemini_process_document(document_file, document_data):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])    

    logger.info("Uploading file")
    file = genai.upload_file(document_file, mime_type="application/pdf")
    while file.state.name == 'PROCESSING':
        logger.debug('Waiting for file to be processed.')
        time.sleep(2)
        file = genai.get_file(file.name)

    logger.info("Creating cache")
    cache =genai.caching.CachedContent.create(
        model="models/gemini-1.5-flash-8b-latest",
        display_name='cached file', # used to identify the cache
        system_instruction=SYSTEM_PROMPT,
        contents=[file],
        ttl=datetime.timedelta(minutes=15),
    )

    logger.info("Creating model")
    model = genai.GenerativeModel.from_cached_content(
        cached_content=cache,
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
    )

    logger.info("Predicting")
    n = 0
    answers = {}
    sections = {}
    for index, row in document_data.iterrows():
        if n > 0 and n % 13 == 0:
            logger.info("Waiting for 60 seconds")
            time.sleep(60)
        question = row["question"]
        logger.debug(f"Question: {question}")
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        question,
                    ],
                }
            ]
        )

        response = chat_session.send_message("INSERT_INPUT_HERE")
        logger.debug(response.text)
        response_json = json.loads(response.text)
        answers[index] = response_json["answer"]
        sections[index] = response_json["section"]
        n += 1
