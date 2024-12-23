from structured_qa.preprocessing import document_to_sections_dir


def test_document_to_sections_dir(tmp_path, example_data):
    output_dir = tmp_path / "output"
    document_to_sections_dir(example_data / "EU_AI_ACT_CHAPTER_V.pdf", output_dir)
    sections = list(output_dir.iterdir())
    assert all(section.is_file() and section.suffix == ".txt" for section in sections)
    assert len(sections) == 6
