from structured_qa.config import ANSWER_PROMPT, FIND_PROMPT
from structured_qa.workflow import find_retrieve_answer


def test_find_retrieve_answer_multi_sections(tmp_path, mocker):
    model = mocker.MagicMock()

    def side_effect(messages):
        if FIND_PROMPT[:10] in messages[0]["content"]:
            if "section_1" in messages[0]["content"]:
                return {"choices": [{"message": {"content": "section_1"}}]}
            else:
                return {"choices": [{"message": {"content": "section_2"}}]}
        elif "Section 1" in messages[0]["content"]:
            return {"choices": [{"message": {"content": "I need more info."}}]}
        elif "Section 2" in messages[0]["content"]:
            return {"choices": [{"message": {"content": "Answer in Section 2"}}]}

    model.create_chat_completion.side_effect = side_effect

    sections_dir = tmp_path / "sections"
    sections_dir.mkdir()
    (sections_dir / "section_1.txt").write_text("Section 1")
    (sections_dir / "section_2.txt").write_text("Section 2")

    question = "What is the answer?"
    answer, sections_checked = find_retrieve_answer(
        model=model,
        sections_dir=sections_dir,
        question=question,
        find_prompt=FIND_PROMPT,
        answer_prompt=ANSWER_PROMPT,
    )

    assert answer == "Answer in Section 2"
    assert sections_checked == ["section_1", "section_2"]


def test_find_retrieve_answer_unkown_section(tmp_path, mocker):
    model = mocker.MagicMock()

    def side_effect(messages):
        if FIND_PROMPT[:10] in messages[0]["content"]:
            return {"choices": [{"message": {"content": "section_x"}}]}

    model.create_chat_completion.side_effect = side_effect

    sections_dir = tmp_path / "sections"
    sections_dir.mkdir()
    (sections_dir / "section_1.txt").write_text("Section 1")

    question = "What is the answer?"
    answer, sections_checked = find_retrieve_answer(
        model=model,
        sections_dir=sections_dir,
        question=question,
        find_prompt=FIND_PROMPT,
        answer_prompt=ANSWER_PROMPT,
    )

    assert answer is None
    assert sections_checked == []
