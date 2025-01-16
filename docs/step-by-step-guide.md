# **Step-by-Step Guide: How the Structured-Q-A Blueprint Works**

Transforming static documents into engaging podcast episodes involves an integration of pre-processing, LLM-powered transcript generation, and text-to-speech generation. Here's how it all works under the hood:

---

## **Overview**

This system has the following core stages:


📑 **1. Document Pre-Processing**
   Prepare the input document by extracting the different sections that compose the structure of the document.
   Split the sections and save them to separate files.

🔎 **2. Find Relevant Section**
   Given a list of sections and the input question, use the LLM to identify the section that looks more relevant.

📄 **3. Retrieve Section**
    Load the individual section to be passed to the next step.

📗 **4. Answer Question**
   Use the LLM to answer the question based on the information available in the retrieved section.


In case the LLM can't find an answer to the question, the stages 2 to 4 run on a loop until the LLM finds the answer.

---

## **Document Pre-Processing**

The process begins with preparing the input document for AI processing.
The document is first converted to markdown and then split into sections based on the markdown headings.

 **Markdown Conversion**

   - Uses [pymupdf4llm](https://pypi.org/project/pymupdf4llm/)

 **Section Splitting**

   - Uses [langchain-text-splitters](https://pypi.org/project/langchain-text-splitters/)

   - Splits on `("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")`

   - Each section is saved to a separate file.

### 🔍 **API Example**

```py
from structured_qa.preprocessing import document_to_sections_dir

section_names = document_to_sections_dir(
    "example_data/1706.03762v7.pdf", "example_outputs/1706.03762v7"
)
print(section_names)
"""
['attention is all you need', '1 introduction', '2 background', '3 model architecture', '4 why self-attention', '5 training', '6 results', '7 conclusion', 'references', 'attention visualizations']
"""
```

## **Find, Retrieve, Answer**

These steps run in a loop until an answer is found or the maximum number of iterations is reached.
An input `model` previously loaded with [`load_llama_cpp_model`](api.md/#structured_qa.model_loaders.load_llama_cpp_model) must
be provided.

The loop is defined in [`find_retrieve_answer`](api.md/#structured_qa.workflow.find_retrieve_answer)

 **Find**

   - Using the `section_names` from the pre-processing, calls the `model` with the [`FIND_PROMPT`](api.md/#structured_qa.config.FIND_PROMPT)

 **Retrieve**

   - Loads the `section` file picked by the `model`.

 **Answer**

   - Calls the `model` with the [`ANSWER_PROMPT`](api.md/#structured_qa.config.ANSWER_PROMPT)

### 🔍 **API Example**

```py
from structured_qa.config import ANSWER_PROMPT, FIND_PROMPT
from structured_qa.model_loaders import load_llama_cpp_model
from structured_qa.workflow import find_retrieve_answer

# Load the model
model = load_llama_cpp_model(
    "bartowski/Qwen2.5-3B-Instruct-GGUF/Qwen2.5-3B-Instruct-f16.gguf"
)

answer, sections_checked = find_retrieve_answer(
    question="What optimizer was using for training?",
    model=model,
    sections_dir="example_outputs/1706.03762v7",
    find_prompt=FIND_PROMPT,
    answer_prompt=ANSWER_PROMPT
)
print(answer)
"""
The optimizer used during training was Adam, with parameters β1 = 0.9, β2 = 0.98, and ϵ = 10^−9.
"""
print(sections_checked)
"""
['5 training']
"""
```

## 🎨 **Customizing the Blueprint**

To better understand how you can tailor this Blueprint to suit your specific needs, please visit the **[Customization Guide](customization.md)**.

## 🤝 **Contributing to the Blueprint**

Want to help improve or extend this Blueprint? Check out the **[Future Features & Contributions Guide](future-features-contributions.md)** to see how you can contribute your ideas, code, or feedback to make this Blueprint even better!
