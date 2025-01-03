from pathlib import Path

import pymupdf4llm
from langchain_text_splitters import MarkdownHeaderTextSplitter

from loguru import logger


@logger.catch(reraise=True)
def document_to_sections_dir(input_file: str, output_dir: str) -> list[str]:
    """
    Convert a document to a directory of sections.

    Uses [pymupdf4llm](https://pypi.org/project/pymupdf4llm/) to convert input_file to markdown.
    Then uses [langchain_text_splitters](https://pypi.org/project/langchain-text-splitters/) to split the markdown into sections based on the headers.

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

    Returns:
        List of section names.
    """

    logger.info(f"Converting {input_file}")
    md_text = pymupdf4llm.to_markdown(input_file)
    logger.success("Converted")

    logger.info("Extracting sections")
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
    )
    sections = splitter.split_text(md_text)
    logger.success(f"Found {len(sections)} sections")

    logger.info(f"Writing sections to {output_dir}")
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    section_names = []
    for section in sections:
        if not section.metadata:
            continue
        section_name = list(section.metadata.values())[-1].lower()
        section_names.append(section_name)
        (output_dir / f"{section_name.replace('/', '_')}.txt").write_text(
            section.page_content
        )
    logger.success("Done")

    return section_names
