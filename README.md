<p align="center">
  <img src="./images/Blueprint-logo-black.png" width="35%" alt="Blueprints Logo"/>
</p>

# Structured-QA: Academic Paper Analysis

> A specialized fork of [Mozilla.ai's Structured-QA Blueprint](https://github.com/mozilla-ai/structured-qa) optimized for analyzing academic papers and research documents.

[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr)
[![Docs](https://github.com/mozilla-ai/structured-qa/actions/workflows/docs.yaml/badge.svg)](https://github.com/mozilla-ai/structured-qa/actions/workflows/docs.yaml/)
[![Tests](https://github.com/mozilla-ai/structured-qa/actions/workflows/tests.yaml/badge.svg)](https://github.com/mozilla-ai/structured-qa/actions/workflows/tests.yaml/)
[![Ruff](https://github.com/mozilla-ai/structured-qa/actions/workflows/lint.yaml/badge.svg?label=Ruff)](https://github.com/mozilla-ai/structured-qa/actions/workflows/lint.yaml/)

This specialized fork demonstrates how to use open-source models and a simple LLM workflow to analyze academic papers and research documents. Key features include:

- 📚 Intelligent parsing and analysis of academic papers with section navigation
- 📊 Preservation of technical content, mathematical notation, and citations
- 🤖 Enhanced comprehension using the Qwen 7B model

A lightweight, open-source solution for answering questions about structured documents using simple LLM workflows, designed as an efficient alternative to complex RAG systems.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexmeckes/academic-paper-structured-qa/main/D3F5F717-26A9-4700-BCD7-9B020484523B.jpeg" width="800" alt="Structured QA App Interface"/>
</p>

<img src="./images/structured-qa-diagram.png" width="1200" alt="structure-qa Diagram" />

📘 To explore the original project and discover other Blueprints, visit the [**Blueprints Hub**](https://developer-hub.mozilla.ai/blueprints/query-structured-documents-using-a-lightweight-llm-workflow).


### 👉 📖 For more detailed guidance on using this project, please visit our [Docs here](https://mozilla-ai.github.io/structured-qa/).


## Quick-start

Get started with academic paper analysis using one of these options:

| Google Colab | HuggingFace Spaces  | GitHub Codespaces |
| -------------| ------------------- | ----------------- |
| [![Try on Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mozilla-ai/structured-qa/blob/main/demo/notebook.ipynb) | [![Try on Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Try%20on-Spaces-blue)](https://huggingface.co/spaces/mozilla-ai/structured-qa) | [![Try on Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=904169776&skip_quickstart=true&machine=standardLinux32gb) |

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/alexmeckes/academic-paper-structured-qa.git
cd academic-paper-structured-qa
pip install -e .
```

2. Launch the academic paper analysis UI:
```bash
python -m streamlit run demo/app.py
```

### Command Line Usage

Install from pip:
```bash
pip install structured-qa
```

Analyze a paper:
```bash
structured-qa \
--question "What were the key findings of this study?" \
--input_file "path/to/your/paper.pdf" \
--output_dir "output/directory"
```

## Key Differences from Original Blueprint

This fork differs from the original Structured-QA Blueprint in several ways:
- Uses the more powerful Qwen 7B model for better academic comprehension
- UI optimized for academic paper analysis
- Enhanced section parsing for research paper structure
- Better handling of technical content and mathematical notation

## Credits

This project is a fork of [Mozilla.ai's Structured-QA Blueprint](https://github.com/mozilla-ai/structured-qa). The original project demonstrates a lightweight approach to document QA without requiring complex RAG systems or large context windows.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To get started, you can check out the [CONTRIBUTING.md](CONTRIBUTING.md) file.
