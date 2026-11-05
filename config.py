#!/usr/bin/env python3
"""
Configuration checks: run them before the agents start, so that
common setup problems give a clear message instead of a long error.
"""
import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv

REQUIRED_VARIABLES = ["OLLAMA_API_BASE", "MODEL_NAME"]


class ConfigError(Exception):
    """
    Raised when the project is not configured correctly.
    """


def load_config():
    """
    Load the .env file and return the required variables as a dict.
    Raise ConfigError if a variable is missing or empty.
    """
    load_dotenv()
    missing = [name for name in REQUIRED_VARIABLES
               if not os.getenv(name, "").strip()]
    if missing:
        raise ConfigError(
            "Missing environment variable(s): " + ", ".join(missing)
            + ".\nCopy .env.example to .env and fill in the values:"
            + "\n    cp .env.example .env"
        )
    return {name: os.getenv(name).strip() for name in REQUIRED_VARIABLES}


def get_ollama_models(api_base):
    """
    Return the list of model names installed in Ollama.
    Raise ConfigError if Ollama cannot be reached.
    """
    url = api_base.rstrip("/") + "/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
    except (urllib.error.URLError, OSError) as error:
        raise ConfigError(
            f"Cannot reach Ollama at {api_base} ({error}).\n"
            "Check that Ollama is running:\n    ollama serve"
        ) from error
    return [model.get("name", "") for model in data.get("models", [])]


def check_model_available(model_name, installed):
    """
    Raise ConfigError if model_name (e.g. 'ollama_chat/llama3.2')
    is not in the list of installed Ollama models.
    """
    name = model_name.split("/", 1)[-1]
    if ":" not in name:
        name += ":latest"
    if name not in installed:
        available = ", ".join(installed) or "none"
        raise ConfigError(
            f"Model '{name}' is not available in Ollama.\n"
            f"Installed models: {available}\n"
            f"Download it with:\n    ollama pull {name}"
        )


def check_config():
    """
    Run every configuration check. Return the config dict if all is OK.
    """
    config = load_config()
    installed = get_ollama_models(config["OLLAMA_API_BASE"])
    check_model_available(config["MODEL_NAME"], installed)
    return config
