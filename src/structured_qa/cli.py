from pathlib import Path

from fire import Fire
from loguru import logger

import yaml

from structured_qa.config import Config
from structured_qa.preprocessing import document_to_sections_dir


@logger.catch(reraise=True)
def structured_qa(
    input_file: str | None = None,
    output_dir: str | None = None,
    from_config: str | None = None,
):
    """ """
    if from_config:
        config = Config.model_validate(yaml.safe_load(Path(from_config).read_text()))
    else:
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        config = Config(input_file=input_file, output_dir=output_dir)

    logger.info("Loading and converting to sections")
    document_to_sections_dir(config.input_file, config.output_dir)
    logger.success("Done")


def main():
    Fire(structured_qa)
