from io import BytesIO
from pathlib import Path

import pymupdf
import streamlit as st
import torch
from llama_cpp import Llama

from structured_qa.preprocessing import document_to_sections_dir
from structured_qa.workflow import find_retrieve_answer


@st.cache_resource
def load_model():
    return Llama.from_pretrained(
        repo_id="MaziyarPanahi/SmolTulu-1.7b-Reinforced-GGUF",
        filename="SmolTulu-1.7b-Reinforced.fp16.gguf",
        n_ctx=0,
        n_gpu_layers=-1 if torch.cuda.is_available() else 0,
        verbose=False,
    )


@st.cache_resource
def convert_to_sections(uploaded_file, output_dir):
    document_to_sections_dir(
        pymupdf.open("type", BytesIO(uploaded_file.read())),
        output_dir,
    )


st.title("Structured Q&A")

st.header("Uploading Data")

uploaded_file = st.file_uploader(
    "Choose a file", type=["pdf", "html", "txt", "docx", "md"]
)

if uploaded_file is not None:
    st.divider()
    st.header("Loading and converting to sections")
    st.markdown("[Docs for this Step]()")
    st.divider()

    convert_to_sections(uploaded_file, f"example_outputs/{uploaded_file.name}")

    sections = [f.stem for f in Path(f"example_outputs/{uploaded_file.name}").iterdir()]
    st.json(sections)

    model = load_model()
    question = st.text_input("Enter a question:")
    if question:
        with st.spinner("Answering..."):
            answer, sections_checked = find_retrieve_answer(
                model=model,
                sections_dir=f"example_outputs/{uploaded_file.name}",
                question=question,
            )
            st.text("Sections checked:")
            st.json(sections_checked)
            st.text("Answer:")
            st.text(answer)
