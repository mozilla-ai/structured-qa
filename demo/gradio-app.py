import gradio as gr
from pathlib import Path

from structured_qa.config import ANSWER_PROMPT, FIND_PROMPT
from structured_qa.model_loaders import load_llama_cpp_model
from structured_qa.preprocessing import document_to_sections_dir
from structured_qa.workflow import find_retrieve_answer


model = load_llama_cpp_model(
    "bartowski/Qwen2.5-3B-Instruct-GGUF/Qwen2.5-3B-Instruct-f16.gguf",
)


def convert_to_sections(uploaded_file):
    output_dir = f"example_outputs/{Path(uploaded_file).name}"
    document_to_sections_dir(
        uploaded_file,
        output_dir,
    )
    sections = [f.stem for f in Path(output_dir).iterdir()]
    return sections, output_dir


def answer_question(uploaded_file, question):
    if not uploaded_file:
        return "Please upload a document first.", None, None
    sections_dir = f"example_outputs/{Path(uploaded_file).name}"
    answer, sections_checked = find_retrieve_answer(
        model=model,
        sections_dir=sections_dir,
        question=question,
        find_prompt=FIND_PROMPT,
        answer_prompt=ANSWER_PROMPT,
    )

    return sections_checked, answer


if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("# Structured Q&A")
        with gr.Tab("Upload Document & Ask a Question"):
            with gr.Row():
                with gr.Column():
                    uploaded_file = gr.File(
                        label="Choose a file",
                        file_types=[".pdf", ".html", ".txt", ".docx", ".md"],
                    )
                with gr.Column():
                    question = gr.Textbox(label="Enter a Question")

            sections_output = gr.JSON(label="Sections")
            sections_checked_output = gr.JSON(label="Sections Checked")
            answer_output = gr.Textbox(label="Answer")

            uploaded_file.upload(
                fn=convert_to_sections,
                inputs=[uploaded_file],
                outputs=[sections_output],
                api_name="convert",
            )
            question.submit(
                fn=answer_question,
                inputs=[uploaded_file, question],
                outputs=[sections_checked_output, answer_output],
                api_name="answer",
            )
    demo.launch()
