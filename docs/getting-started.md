Get started with Structured-Q-A using one of the options below:

---

## Setup options

=== "☁️ Google Colab (GPU)"

      The easiest way to play with the code on a GPU, for free.

      Click the button below to launch the project directly in Google Colab:

      <p align="center"><a href="https://colab.research.google.com/github/mozilla-ai/document-to-podcast/blob/main/demo/notebook.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" /></a></p>

=== "☁️ GitHub Codespaces"

      Click the button below to launch the project directly in GitHub Codespaces:

      <p align="center"><a href="https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=904169776&skip_quickstart=true&machine=standardLinux32gb"><img src="https://github.com/codespaces/badge.svg" /></a></p>

      Once the Codespaces environment launches, inside the terminal, start the Streamlit demo by running:

      ```bash
      python -m streamlit run demo/app.py
      ```

=== "💻 Local Installation"

      You can install the project from Pypi:

      ```bash
      pip install structured-q-a
      ```

      Check the [Command Line Interface](./cli.md) guide.

      ---

      Alternatively, you can clone and install it in editable mode:

      1. **Clone the Repository**

         ```bash
         git clone https://github.com/mozilla-ai/structured-q-a.git
         cd structured-q-a
         ```

      2. **Install the project and its Dependencies**

         ```bash
         pip install -e .
         ```

      3. **Run the Demo**

         ```bash
         python -m streamlit run demo/app.py
         ```
