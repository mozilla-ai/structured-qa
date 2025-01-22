import subprocess

from llama_cpp import Llama
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template


def gpu_available():
    try:
        subprocess.check_output("nvidia-smi")
        return True
    except Exception:
        return False


def load_llama_cpp_model(model_id: str) -> Llama:
    """
    Loads the given model_id using Llama.from_pretrained.

    Examples:
        >>> model = load_llama_cpp_model("allenai/OLMoE-1B-7B-0924-Instruct-GGUF/olmoe-1b-7b-0924-instruct-q8_0.gguf")

    Args:
        model_id (str): The model id to load.
            Format is expected to be `{org}/{repo}/{filename}`.

    Returns:
        Llama: The loaded model.
    """
    org, repo, filename = model_id.split("/")
    model = Llama.from_pretrained(
        repo_id=f"{org}/{repo}",
        filename=filename,
        n_ctx=0,  # 0 means that the model limit will be used, instead of the default (512) or other hardcoded value
        verbose=False,
        n_gpu_layers=-1 if gpu_available() else 0,
    )
    return model


class UnslothModel:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def create_chat_completion(self, messages):
        inputs = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to("cuda")
        outputs = self.model.generate(input_ids=inputs)
        response = self.tokenizer.batch_decode(
            outputs[:, len(inputs[0]) :], skip_special_tokens=True
        )[0]
        return response


def load_unsloth_model(
    model_id: str, chat_template: str, load_in_4bit: bool = True, **kwargs
) -> UnslothModel:
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_id,
        load_in_4bit=load_in_4bit,
        **kwargs,
    )
    tokenizer = get_chat_template(
        tokenizer,
        chat_template=chat_template,
    )
    FastLanguageModel.for_inference(model)
    return UnslothModel(model=model, tokenizer=tokenizer)
