from io import BytesIO
from pathlib import Path

import pymupdf
import streamlit as st

from structured_qa.config import ANSWER_PROMPT, FIND_PROMPT
from structured_qa.model_loaders import load_llama_cpp_model
from structured_qa.preprocessing import document_to_sections_dir
from structured_qa.workflow import find_retrieve_answer


@st.cache_resource
def load_model():
    return load_llama_cpp_model(
        "bartowski/Qwen2.5-7B-Instruct-GGUF/Qwen2.5-7B-Instruct-Q8_0.gguf"
    )


@st.cache_resource
def convert_to_sections(uploaded_file, output_dir):
    document_to_sections_dir(
        pymupdf.open("type", BytesIO(uploaded_file.read())),
        output_dir,
    )


st.title("📚 Academic Paper Analysis")
st.markdown("""
A tool that helps you analyze academic papers by breaking them down into sections and answering your questions while preserving technical details and academic rigor.
""")

st.header("📄 Upload Your Paper")

uploaded_file = st.file_uploader(
    "Upload an academic paper (PDF format recommended for best results)", 
    type=["pdf", "html", "txt", "docx", "md"]
)

if uploaded_file is not None:
    st.divider()
    st.header("🔍 Paper Structure Analysis")
    st.markdown("Analyzing the paper's structure and extracting sections...")
    st.divider()

    convert_to_sections(uploaded_file, f"example_outputs/{uploaded_file.name}")

    sections = [f.stem for f in Path(f"example_outputs/{uploaded_file.name}").iterdir()]
    st.subheader("📑 Extracted Sections")
    st.json(sections)

    model = load_model()
    question = st.text_input("🤔 What would you like to know about this paper?")
    if question:
        with st.spinner("Analyzing the paper..."):
            answer, sections_checked = find_retrieve_answer(
                model=model,
                sections_dir=f"example_outputs/{uploaded_file.name}",
                question=question,
                find_prompt=FIND_PROMPT,
                answer_prompt=ANSWER_PROMPT,
            )
            st.subheader("🔎 Sections Referenced")
            st.json(sections_checked)
            st.subheader("💡 Answer")
            st.markdown(answer)
