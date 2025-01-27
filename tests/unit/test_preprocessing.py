import pytest

from structured_qa.preprocessing import split_markdown_by_headings
from structured_qa.preprocessing import document_to_sections_dir


def test_document_to_sections_dir(tmp_path, example_data):
    output_dir = tmp_path / "output"
    document_to_sections_dir(example_data / "1706.03762v7.pdf", output_dir)
    sections = list(output_dir.iterdir())
    assert all(section.is_file() and section.suffix == ".txt" for section in sections)
    assert len(sections) == 12


DEFAULT_HEADINGS = """
# Introduction

This is the introduction.

## Related Work

This is the related work.

### Method

This is the method.
"""

NUMERIC_HEADINGS = """
**1.** **Introduction**

This is the introduction.

**2.** **Related Work**

This is the related work.

**2.1** **Method**

This is the method.
"""


@pytest.mark.parametrize(
    ("markdown_text", "n_sections"),
    (
        (DEFAULT_HEADINGS, 3),
        (NUMERIC_HEADINGS, 2),
    ),
)
def test_split_markdown_by_headings(markdown_text, n_sections):
    sections = split_markdown_by_headings(markdown_text)
    assert len(sections) == n_sections
