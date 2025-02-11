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
    return document_to_sections_dir(
        pymupdf.open("type", BytesIO(uploaded_file.read())),
        output_dir,
    )


st.title("Structured QA")

st.header("Uploading Data")

uploaded_file = st.file_uploader(
    "Choose a file", type=["pdf", "html", "txt", "docx", "md"]
)

if uploaded_file is not None:
    st.divider()
    st.header("Loading and converting to sections")
    st.markdown("[Docs for this Step]()")
    st.divider()

    try:
        with st.spinner("Converting document to sections..."):
            section_names = convert_to_sections(uploaded_file, f"example_outputs/{uploaded_file.name}")
            sections = [f.stem for f in Path(f"example_outputs/{uploaded_file.name}").iterdir()]
            
            # Provide feedback about segmentation
            st.success(f"Successfully extracted {len(sections)} sections from the document.")
            
            # Check for potential segmentation issues
            if len(sections) == 1:
                st.warning("⚠️ Only one section was found. This might indicate that the document structure wasn't properly detected.")
            elif len(sections) == 0:
                st.error("❌ No sections were found in the document. The document might not have a clear structure or might be in an unsupported format.")
            elif "INTRO" in sections and len(sections) < 3:
                st.warning("⚠️ Only found default sections. The document structure might not have been properly detected.")
            
            # Show sections
            st.text("Detected Sections:")
            st.json(sections)

            model = load_model()
            question = st.text_input("Enter a question:")
            if question:
                with st.spinner("Answering..."):
                    answer, sections_checked = find_retrieve_answer(
                        model=model,
                        sections_dir=f"example_outputs/{uploaded_file.name}",
                        question=question,
                        find_prompt=FIND_PROMPT,
                        answer_prompt=ANSWER_PROMPT,
                    )
                    st.text("Sections checked:")
                    st.json(sections_checked)
                    st.text("Answer:")
                    st.text(answer)
    except Exception as e:
        st.error(f"❌ Error processing document: {str(e)}")
        st.info("💡 Try uploading a different document or check if the file is corrupted.")
