# Command Line Interface

Once you have [installed the blueprint](./getting-started.md), you can use it from the CLI.

You can either provide the path to a configuration file:

```bash
structured-qa --from_config "example_data/config.yaml"
```

Or provide values to the arguments directly:


```bash
structured-aq \
--input_file "example_data/EU_AI_ACT_CHAPTER_V.pdf" \
--output_folder "example_outputs/EU_AI_ACT_CHAPTER_V"
```

---

::: structured_qa.cli.structured_qa

---

::: structured_qa.config.Config
