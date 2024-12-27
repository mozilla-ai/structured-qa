# Command Line Interface

Once you have [installed the blueprint](./getting-started.md), you can use it from the CLI.

You can either provide the path to a configuration file:

```bash
structured-qa --from_config "example_data/config.yaml"
```

Or provide values to the arguments directly:


```bash
structured-qa \
--question "What learning rate was used?" \
--input_file "example_data/1706.03762v7.pdf" \
--output_folder "example_outputs/1706.03762v7.pdf"
```

---

::: structured_qa.cli.structured_qa

---

::: structured_qa.config.Config
