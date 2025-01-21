from pathlib import Path
from urllib.request import urlretrieve
from typing import Callable

import pandas as pd
from fire import Fire
from loguru import logger


def download_document(url, output_file):
    if not Path(output_file).exists():
        urlretrieve(url, output_file)
        logger.debug(f"Downloaded {url} to {output_file}")
    else:
        logger.debug(f"File {output_file} already exists")


@logger.catch(reraise=True)
def run_benchmark(
    input_data: str, output_file: str, process_document: Callable, **kwargs
):
    logger.info("Loading input data")
    data = pd.read_csv(input_data)
    data["pred_answer"] = [None] * len(data)
    data["pred_section"] = [None] * len(data)

    for document_link, document_data in data.groupby("document"):
        logger.info(f"Downloading document {document_link}")
        downloaded_document = Path(f"{Path(document_link).name}.pdf")
        download_document(document_link, downloaded_document)

        answers, sections = process_document(
            downloaded_document, document_data, **kwargs
        )

        for index in document_data.index:
            data.loc[index, "pred_answer"] = str(answers[index]).upper()
            data.loc[index, "pred_section"] = sections[index]

    data.to_csv(output_file)


if __name__ == "__main__":
    Fire(run_benchmark)
