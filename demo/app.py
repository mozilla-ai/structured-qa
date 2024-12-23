from io import BytesIO
from pathlib import Path

import streamlit as st
from docling_core.types.io import DocumentStream
from structured_qa.preprocessing import document_to_sections_dir

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

    with st.spinner("Converting to sections..."):
        document_to_sections_dir(
            DocumentStream(
                name=uploaded_file.name, stream=BytesIO(uploaded_file.read())
            ),
            "output",
        )

    sections = [f.stem for f in Path("output").iterdir()]
    st.json(sections)
