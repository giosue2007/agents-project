# Agents Project

A local multi-agent project built with Google ADK, LiteLLM and Ollama.
Given a topic, it generates a Markdown study guide and saves it in
`output/`.

## Architecture

    Google ADK -> LiteLLM -> Ollama -> Local model

## Workflow

    Topic input
    -> Explainer Agent
    -> Practice Designer Agent
    -> Draft Study Guide
    -> Reviewer Agent
    -> Final Markdown Assembly
    -> Validation Tool
    -> Save Markdown Tool

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

    ollama pull llama3.2

### 5. Check that the model responds

    ollama run llama3.2 "Say hello in one sentence."

If Ollama is not running, start it with `ollama serve`.

### 6. Configure the environment

    cp .env.example .env

| Variable          | Description                                   |
|-------------------|-----------------------------------------------|
| `OLLAMA_API_BASE` | URL of the local Ollama server                |
| `MODEL_NAME`      | Model used by LiteLLM (`ollama_chat/<model>`) |

The real `.env` file is never committed.

## Model used

`llama3.2` (3b, about 2 GB), pulled with Ollama.
`llama3.2:1b` is faster but follows the instructions less reliably.

## Usage

    python3 main.py "Python list comprehensions"

The guide is saved in `output/python_list_comprehensions.md`.

## Troubleshooting

The project checks the input and the configuration before running
the agents. It exits with status `1` and a readable message when
something is wrong.

### Empty topic

    $ python3 main.py ""
    Error: Topic cannot be empty.
    Usage: python3 main.py "<topic>"

Give a topic between quotes.

### Missing environment variables

    Error: Missing environment variable(s): MODEL_NAME.
    Copy .env.example to .env and fill in the values:
        cp .env.example .env

Create the `.env` file and check that both variables have a value.

### Ollama not running

    Error: Cannot reach Ollama at http://localhost:11434 (...).
    Check that Ollama is running:
        ollama serve

Start Ollama in another terminal, or check `OLLAMA_API_BASE`.

### Model not available

    Error: Model 'llama3.2:latest' is not available in Ollama.
    Installed models: llama3.2:1b
    Download it with:
        ollama pull llama3.2:latest

Pull the model, or change `MODEL_NAME` in `.env` to an installed one
(list them with `ollama list`).

### File-writing error

    Error: could not save output/guide.md: [Errno 13] Permission denied

Check that you can write in the `output/` directory.

### Validation failure

    Validation FAILED: missing sections -> Common Mistakes
    The guide is still saved so you can inspect it. Try running the
    command again.

Local models do not always follow the format. The guide is saved
anyway; run the command again or try a bigger model.

### Other errors

Unexpected errors are not hidden: Python prints the full traceback,
which is useful to find the real cause during development.
