# AI Agents in Python

## Description

This project generates a short **study guide** for a programming topic
using several AI agents that run **locally**, with no paid API.

Given a topic such as `"Python list comprehensions"`, three agents work
one after the other, then deterministic Python tools validate the result
and save it as a Markdown file in `output/`.

The stack is:

    Google ADK  ->  LiteLLM  ->  Ollama  ->  Local model (llama3.2)

- **Google ADK** defines and runs the agents.
- **LiteLLM** connects ADK to the model provider.
- **Ollama** runs the model on the local machine.

## Requirements

- Python 3.10 or newer (tested with Python 3.12)
- Ollama (tested with version 0.40.14)
- About 2 GB of free disk space for the `llama3.2` model
- Linux, macOS, or Windows with WSL (tested on Windows + WSL 2,
  Ubuntu 24.04)

Python dependencies (in `requirements.txt`):

- `google-adk`
- `litellm`
- `python-dotenv`

## Setup

1. Create and activate a virtual environment:

        python3 -m venv .venv
        source .venv/bin/activate

2. Install the Python dependencies:

        pip install -r requirements.txt

3. Install Ollama (see https://ollama.com/download). On Ubuntu:

        sudo apt-get install zstd
        curl -fsSL https://ollama.com/install.sh | sh

4. Pull the model:

        ollama pull llama3.2

5. Check that the model responds before running the project:

        ollama run llama3.2 "Say hello in one sentence."

## Configuration

Copy the example file and adjust the values if needed:

    cp .env.example .env

| Variable          | Example value             | Description                      |
|-------------------|---------------------------|----------------------------------|
| `OLLAMA_API_BASE` | `http://localhost:11434`  | URL of the local Ollama server   |
| `MODEL_NAME`      | `ollama_chat/llama3.2`    | Model used by LiteLLM            |

The `ollama_chat/` prefix tells LiteLLM to use Ollama's chat API.
The real `.env` file is listed in `.gitignore` and is never committed.
No API key is needed.

## How to Run

Make sure Ollama is running (`ollama serve` if needed), then:

    source .venv/bin/activate
    python3 main.py "Python list comprehensions"

If no topic is given, the program asks for one. Before calling the
agents, it checks the topic and the configuration (variables, Ollama
server, model) and stops with a clear message if something is wrong.

## Example Input

    python3 main.py "Python list comprehensions"

## Example Output

Terminal:

    Checking configuration...
    Configuration OK (model: ollama_chat/llama3.2)

    [1/5] Explainer Agent: writing the explanation...
    [2/5] Practice Designer Agent: creating the exercise...
    [3/5] Assembling the draft study guide...
    [4/5] Reviewer Agent: reviewing the draft...
    [5/5] Assembling the final Markdown...

    Validation Tool: checking required sections...
    Validation: OK, all required sections are present.
    Save Markdown Tool: writing the file...
    Saved to output/python_list_comprehensions.md

Extract of `output/python_list_comprehensions.md`:

    # Topic

    Python list comprehensions

    ## Simple Explanation
    Python list comprehensions are a concise way to create new lists
    by performing operations on existing lists or other iterables.

    ## Key Concepts
    * Expression: the operation applied to each item.
    * Iteration: applying the expression to each item of an iterable.
    * Filtering: keeping items that match a condition.

    ## Example
    numbers = [1, 2, 3, 4, 5]
    squared_numbers = [x**2 for x in numbers]   # [1, 4, 9, 16, 25]

    ## Practice Exercise
    ...
    ## Common Mistakes
    ...
    ## Review Comments
    ...
    **Recommendation:** NEEDS REVISION, ...

    ## Final Summary
    ...

## Project Structure

    .
    ├── agents/
    │   ├── __init__.py
    │   ├── explainer_agent.py          # Explainer Agent
    │   ├── practice_designer_agent.py  # Practice Designer Agent
    │   └── reviewer_agent.py           # Reviewer Agent
    ├── tools/
    │   ├── __init__.py
    │   ├── file_writer.py              # save_markdown_file()
    │   └── validation.py               # validate_required_sections()
    ├── data/                           # input data (empty for now)
    ├── output/                         # generated study guides
    ├── config.py                       # configuration checks
    ├── main.py                         # sequential workflow
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    └── README.md

## Agents

| Agent | File | Input | Output |
|-------|------|-------|--------|
| Explainer | `agents/explainer_agent.py` | the topic | Simple Explanation, Key Concepts, Example |
| Practice Designer | `agents/practice_designer_agent.py` | topic + explanation | Practice Exercise (with expected input/output and hints), Common Mistakes |
| Reviewer | `agents/reviewer_agent.py` | the draft guide | Review Comments: missing info, unclear parts, suggestions, APPROVED / NEEDS REVISION |

Each agent has one responsibility and its own instructions. The
"Topic" and "Final Summary" sections are written by Python code, not
by a model, so they are always present.

## Tools

| Tool | File | Role |
|------|------|------|
| `save_markdown_file(file_path, content)` | `tools/file_writer.py` | Creates the parent folder if needed, writes the file, returns `Saved to ...` or an `Error: ...` message |
| `validate_required_sections(markdown)` | `tools/validation.py` | Checks that the 8 required headings exist and returns `{"valid": bool, "missing": [...]}` |

The tools are plain Python functions, independent from ADK, so they
always behave the same way and can be tested alone.

## Self-Validation Checklist

- [x] The project structure separates agents, tools, data and output.
- [x] A virtual environment is used and dependencies are listed.
- [x] Ollama is installed and the local model responds.
- [x] The Explainer Agent returns a structured explanation.
- [x] `save_markdown_file()` writes the guide in `output/`.
- [x] `validate_required_sections()` reports missing sections.
- [x] The Practice Designer Agent uses the explanation as context.
- [x] The Reviewer Agent comments without rewriting the guide.
- [x] `main.py` runs the full sequential workflow.
- [x] Common problems (empty topic, missing variables, Ollama not
      running, missing model, file error, validation failure) give a
      readable message.
- [x] No secrets or virtual environment are committed.

## Reflection

**1. What is the difference between a direct LLM call and an AI agent?**

A direct LLM call sends one prompt and gets one answer: the model has
no role, no defined responsibility and nothing checks its output. An
agent wraps the model with a name, a role and precise instructions,
and is run by a framework (ADK) inside a session. In this project the
agents are also chained: the output of one becomes the input of the
next, and deterministic tools check and save the result.

**2. What role does each agent have in your system?**

- The **Explainer Agent** explains the topic simply, with key
  concepts and one example.
- The **Practice Designer Agent** reads that explanation and creates a
  small exercise with expected input/output, hints and common mistakes.
  It does not explain the topic again.
- The **Reviewer Agent** reads the whole draft and gives short,
  specific comments and a recommendation. It does not rewrite the guide.

**3. What role does each tool have in your system?**

- `save_markdown_file()` writes the final guide to `output/` and
  reports errors clearly.
- `validate_required_sections()` checks the structure of the guide.
  It does not judge the content, only that every required heading is
  there.

Both are deterministic: unlike the model, they give the same result
every time for the same input.

**4. What was the most difficult part of the project?**

Setting up the environment (virtual environment, Ollama and its
`zstd` dependency, choosing a model) and getting the agents to follow
a fixed format. The small model often changed the headings (`##` vs
`###`) or forgot parts of the instructions, so the prompts had to
describe the expected structure very precisely and the validator had
to accept small variations.

**5. What limitation did you observe when using your selected model?**

With `llama3.2:1b` the agents often ignored part of the instructions
(for example the exercise had no hints) and made factual mistakes (it
said list comprehensions use parentheses). Switching to `llama3.2`
(3b) gave a much better structure, but it is slower and still makes
logic mistakes: in one run the exercise asked for the even numbers of
`[1, 3, 5, 7, 9]` and gave `[4, 16]` as the expected output. The same
topic also gives a different answer at each run.

## Known Limitations

- **Content is not verified.** The validator only checks headings; a
  section can be present but wrong. The Reviewer Agent catches some
  problems, but not all of them, and nothing fixes them automatically.
- **Format is not always respected.** A local model may skip a section
  or rename a heading; the validation then fails and the command must
  be run again.
- **Non-deterministic output.** Each run produces a different guide.
- **Speed depends on the hardware.** On my laptop (Windows + WSL 2),
  a full run with `llama3.2` (3 agents) takes about one to two
  minutes. Bigger models would be more accurate but slower, and need
  more RAM.
- **English only.** The prompts are written in English and the guide
  is generated in English.
- **No revision loop.** A `NEEDS REVISION` recommendation is reported
  in the guide but does not trigger a new generation.
