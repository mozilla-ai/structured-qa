from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd
from fire import Fire
from loguru import logger


from gemini import gemini_process_document


def download_document(url, output_file):
    if not Path(output_file).exists():
        urlretrieve(url, output_file)
        logger.debug(f"Downloaded {url} to {output_file}")
    else:
        logger.debug(f"File {output_file} already exists")


@logger.catch(reraise=True)
def run_benchmark(input_data: str, output_file: str, model: str):
    logger.info("Loading input data")
    data = pd.read_csv(input_data)
    data["pred_answer"] = [None] * len(data)
    data["pred_section"] = [None] * len(data)


    for document_link, document_data in data.groupby("document"):
        logger.info(f"Downloading document {document_link}")
        downloaded_document = Path(f"example_data/{Path(document_link).name}.pdf")
        download_document(document_link, downloaded_document)

        if model == "gemini":
            answers, sections = gemini_process_document(downloaded_document, document_data)

        for index in document_data.index:
            data.loc[index, "pred_answer"] = answers[index]
            data.loc[index, "pred_section"] = sections[index]
    
    data.to_csv(output_file)

if __name__ == "__main__":
    Fire(run_benchmark)
