<p align="center">
  <picture>
    <!-- When the user prefers dark mode, show the white logo -->
    <source media="(prefers-color-scheme: dark)" srcset="./images/Blueprint-logo-white.png">
    <!-- When the user prefers light mode, show the black logo -->
    <source media="(prefers-color-scheme: light)" srcset="./images/Blueprint-logo-black.png">
    <!-- Fallback: default to the black logo -->
    <img src="./images/Blueprint-logo-black.png" width="35%" alt="Project logo"/>
  </picture>
</p>

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
[![llama.cpp](https://img.shields.io/badge/llama.cpp-E76F00?logo=cplusplus&logoColor=white&labelColor=1E1E1E)](https://github.com/ggml-org/llama.cpp)
[![pymupdf4llm](https://img.shields.io/badge/pymupdf4llm-blue)](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/index.html)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr) <br>
[![Docs](https://github.com/mozilla-ai/structured-qa/actions/workflows/docs.yaml/badge.svg)](https://github.com/mozilla-ai/structured-qa/actions/workflows/docs.yaml/)
[![Tests](https://github.com/mozilla-ai/structured-qa/actions/workflows/tests.yaml/badge.svg)](https://github.com/mozilla-ai/structured-qa/actions/workflows/tests.yaml/)
[![Ruff](https://github.com/mozilla-ai/structured-qa/actions/workflows/lint.yaml/badge.svg?label=Ruff)](https://github.com/mozilla-ai/structured-qa/actions/workflows/lint.yaml/)

[Blueprints Hub](https://developer-hub.mozilla.ai/)
| [Documentation](https://mozilla-ai.github.io/structured-qa/)
| [Getting Started](https://mozilla-ai.github.io/structured-qa/getting-started/)
| [Contributing](CONTRIBUTING.md)

</div>

# Structured-QA: a Blueprint by Mozilla.ai for answering questions about structured documents.

This Blueprint demonstrates how to use open-source models and a simple LLM workflow to answer questions based on structured documents.

It is designed to showcase a simpler alternative to more complex and/or resource-demanding alternatives, such as RAG systems that rely on vector databases and/or long-context models with large token windows.

<img src="./images/structured-qa-diagram.png" width="1200" alt="Structured QA Diagram" />


## Quick-start

Get started with structured-qa using one of the options below:

| Google Colab | HuggingFace Spaces  | GitHub Codespaces |
| -------------| ------------------- | ----------------- |
| [![Try on Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mozilla-ai/structured-qa/blob/main/demo/notebook.ipynb) | [![Try on Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Try%20on-Spaces-blue)](https://huggingface.co/spaces/mozilla-ai/structured-qa) | [![Try on Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=904169776&skip_quickstart=true&machine=standardLinux32gb) |

You can also install and use the blueprint locally:


### Command Line Interface

```bash
pip install structured-qa
```

```bash
structured-qa \
--question "What optimizer was used to train the model?" \
--input_file "example_data/1706.03762v7.pdf" \
--output_dir "example_outputs/1706.03762v7.pdf"
```

### Graphical Interface App

```bash
git clone https://github.com/mozilla-ai/structured-qa.git
cd structured-qa
pip install -e .
```

```bash
python -m streamlit run demo/app.py
```


## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To get started, you can check out the [CONTRIBUTING.md](CONTRIBUTING.md) file.
