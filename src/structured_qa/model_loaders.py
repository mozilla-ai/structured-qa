import subprocess
from llama_cpp import Llama


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
