# 🎨 **Customization Guide**

This Blueprint is designed to be flexible and easily adaptable to your specific needs. This guide will walk you through some key areas you can customize to make the Blueprint your own.

---

## 🖋️ **Customizable Parameters**

-- **`question`**: The question to be answered.

- **`input_file`**: The input file specifies the document to be processed. Supports the `pdf` format.

- **`output_dir`**: Path to the output directory where the extracted sections will be saved.

- **`model`**: Any model that can be loaded by [`LLama.from_pretrained`](https://llama-cpp-python.readthedocs.io/en/latest/#pulling-models-from-hugging-face-hub) can be used here. Format is expected to be `{org}/{repo}/{filename}`. For example: `Qwen/Qwen2.5-1.5B-Instruct-GGUF/qwen2.5-1.5b-instruct-q8_0.gguf`.

- **`find_prompt`**:The prompt for finding the section. See [`FIND_PROMPT`][structured_qa.config.FIND_PROMPT].

- **`answer_prompt`**: The prompt for answering the question.See [`ANSWER_PROMPT`][structured_qa.config.ANSWER_PROMPT].

## ⌨️ **Customizing When Running via the CLI**

If you’re running the pipeline from the command line, you can customize the parameters by modifying the **`example_data/config.yaml`** file.

Running in the CLI:
```bash
structured-qa --from_config example_data/config.yaml
```

### Steps to Customize
1. Open the `config.yaml` file.
2. Locate the parameter you want to adjust.
3. Update the value and save the file.

#### Example: Changing the Text-to-Text Model
In `config.yaml`, modify the `model` entry:

```yaml
model: "Qwen/Qwen2.5-1.5B-Instruct-GGUF/qwen2.5-1.5b-instruct-q8_0.gguf"
```


## 🤝 **Contributing to the Blueprint**

Want to help improve or extend this Blueprint? Check out the **[Future Features & Contributions Guide](future-features-contributions.md)** to see how you can contribute your ideas, code, or feedback to make this Blueprint even better!
