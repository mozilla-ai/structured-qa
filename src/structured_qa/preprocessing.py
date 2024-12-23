from collections import defaultdict
from pathlib import Path

from docling.document_converter import DocumentConverter
from docling_core.types.doc.document import TextItem, SectionHeaderItem

from loguru import logger


@logger.catch(reraise=True)
def document_to_sections_dir(input_file: str, output_dir: str) -> list[str]:
    """
    Convert a document to a directory of sections.

    Uses [docling](https://ds4sd.github.io/docling/) to extract the list of sections from the input document.

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
    converter = DocumentConverter()
    logger.info(f"Converting {input_file}")
    converted = converter.convert(input_file)
    logger.success("Converted")

    logger.info("Extracting sections")
    sections = defaultdict(list)
    current_section = "discard"
    for item, _ in converted.document.iterate_items():
        if isinstance(item, SectionHeaderItem):
            logger.info(f"Found section: {item.text}")
            current_section = item.text.lower().strip()
        elif isinstance(item, TextItem):
            sections[current_section].append(item.text)
    sections.pop("discard", None)

    logger.success(f"Found {len(sections)} sections")

    logger.info(f"Writing sections to {output_dir}")
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    for k, v in sections.items():
        (output_dir / f"{k.replace('/', '_')}.txt").write_text("\n".join(v))
    logger.success("Done")

    return list(sections.keys())
