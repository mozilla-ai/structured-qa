from loguru import logger

from structured_qa.config import FIND_PROMPT, ANSWER_PROMPT
from structured_qa.model_loaders import load_llama_cpp_model
from structured_qa.preprocessing import document_to_sections_dir
from structured_qa.workflow import find_retrieve_answer


def workflow_process_document(
    document_file,
    document_data,
    model_id: str = "bartowski/Qwen2.5-7B-Instruct-GGUF/Qwen2.5-7B-Instruct-Q8_0.gguf",
    find_prompt: str = FIND_PROMPT,
    answer_prompt: str = ANSWER_PROMPT,
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
        logger.info(f"Question: {question}")
        answer, sections_checked = find_retrieve_answer(
            question, model, sections_dir, find_prompt, answer_prompt
        )

        answers[index] = answer
        sections[index] = sections_checked[-1]

    return answers, sections
