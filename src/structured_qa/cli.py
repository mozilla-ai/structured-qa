from pathlib import Path

import yaml
import torch
from fire import Fire
from llama_cpp import Llama
from loguru import logger

from structured_qa.config import Config
from structured_qa.preprocessing import document_to_sections_dir
from structured_qa.workflow import find_retrieve_answer, ANSWER_PROMPT, FIND_PROMPT


@logger.catch(reraise=True)
def structured_qa(
    question: str,
    input_file: str | None = None,
    output_dir: str | None = None,
    model: str | None = "Qwen/Qwen2.5-3B-Instruct-GGUF/Qwen2.5-3B-Instruct-f16.gguf",
    find_prompt: str = FIND_PROMPT,
    answer_prompt: str = ANSWER_PROMPT,
    from_config: str | None = None,
):
    """
    Structured Question Answering.

    Split the input document into sections and answer the question based on the sections.

    Args:
        input_file: Path to the input document.
        output_dir: Path to the output directory.
            Structure of the output directory:

            ```
            output_dir/
                section_1.txt
                section_2.txt
                ...
            ```
        model: Model identifier formatted as `owner/repo/file`.
            Must be hosted at the HuggingFace Hub in GGUF format.
        question: The question to answer.
        find_prompt: The prompt to find the section.
        answer_prompt: The prompt to answer the question.
        from_config: The path to the config file.

            If provided, all other arguments will be ignored.
    """
    if from_config:
        raw_config = yaml.safe_load(Path(from_config).read_text())
        Path(raw_config["output_dir"]).mkdir(exist_ok=True, parents=True)
        config = Config.model_validate(raw_config)
    else:
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        config = Config(
            input_file=input_file,
            output_dir=output_dir,
            model=model,
            find_prompt=find_prompt,
            answer_prompt=answer_prompt,
        )

    logger.info("Loading and converting to sections")
    document_to_sections_dir(config.input_file, config.output_dir)
    logger.success("Done")

    logger.info("Loading Model")
    org, repo, filename = config.model.split("/")
    model = Llama.from_pretrained(
        repo_id=f"{org}/{repo}",
        filename=filename,
        n_ctx=0,
        n_gpu_layers=-1 if torch.cuda.is_available() else 0,
        verbose=False,
    )
    logger.success("Done")

    logger.info("Answering")
    answer, sections_checked = find_retrieve_answer(
        model=model,
        sections_dir=config.output_dir,
        question=question,
        find_prompt=config.find_prompt,
        answer_prompt=config.answer_prompt,
    )
    logger.success("Done")

    logger.info("Sections checked:")
    logger.info(sections_checked)
    logger.info("Answer:")
    logger.info(answer)


def main():
    Fire(structured_qa)
