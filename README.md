# Agents Project

A local AI agent project built with Google ADK, LiteLLM and Ollama.

## Architecture

Google ADK -> LiteLLM -> Ollama -> Local model

## Setup

### 1. Create and activate a virtual environment

    python3 -m venv .venv
    source .venv/bin/activate

### 2. Install Python dependencies

    pip install -r requirements.txt

### 3. Install Ollama

    curl -fsSL https://ollama.com/install.sh | sh

On Ubuntu, `zstd` may be required first: `sudo apt-get install zstd`.
See https://ollama.com/download for other systems.

### 4. Pull a local model

    ollama pull llama3.2:1b

### 5. Check that the model responds

    ollama run llama3.2:1b "Say hello in one sentence."

If Ollama is not running, start it with `ollama serve`.

### 6. Configure the environment

    cp .env.example .env

| Variable          | Description                                   |
|-------------------|-----------------------------------------------|
| `OLLAMA_API_BASE` | URL of the local Ollama server                |
| `MODEL_NAME`      | Model used by LiteLLM (`ollama_chat/<model>`) |

The real `.env` file is never committed.
