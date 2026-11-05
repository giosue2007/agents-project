#!/usr/bin/env python3
"""
Entry point: build a complete study guide for a topic.

Workflow:
    Topic -> Explainer -> Practice Designer -> Draft -> Reviewer
    -> Final Markdown -> Validation -> Save

Usage:
    python3 main.py "Python decorators"
"""
import asyncio
import re
import sys

from google.adk.runners import InMemoryRunner
from google.genai import types

from config import ConfigError, check_config
from agents.explainer_agent import explainer_agent
from agents.practice_designer_agent import practice_designer_agent
from agents.reviewer_agent import reviewer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

APP_NAME = "agents_project"
USER_ID = "student"
OUTPUT_DIR = "output"


# ---------- Input ----------

def get_topic():
    """
    Return the topic from the command line, or ask the user for it.
    Raise ValueError if the topic is empty.
    """
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Topic: ")
    if not topic.strip():
        raise ValueError(
            "Topic cannot be empty.\n"
            "Usage: python3 main.py \"<topic>\""
        )
    return topic.strip()


def topic_to_filename(topic):
    """
    Turn a topic into a safe file name, e.g. 'Python decorators'
    becomes 'python_decorators.md'.
    """
    name = re.sub(r"[^a-z0-9]+", "_", topic.lower()).strip("_")
    return (name or "study_guide") + ".md"


# ---------- Agents ----------

async def run_agent(agent, text):
    """
    Send text to an agent and return its final answer as a string.
    """
    runner = InMemoryRunner(agent=agent, app_name=APP_NAME)
    session = await runner.session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )
    message = types.Content(role="user", parts=[types.Part(text=text)])

    answer = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session.id, new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            answer = "".join(part.text or "" for part in event.content.parts)
    return answer.strip()


async def run_explainer_agent(topic):
    """
    Return the explanation, key concepts and example for the topic.
    """
    return await run_agent(explainer_agent, topic)


async def run_practice_designer_agent(topic, explanation):
    """
    Return a practice exercise and common mistakes, based on
    the topic and the explanation.
    """
    request = f"Topic: {topic}\n\nExplanation:\n{explanation}"
    return await run_agent(practice_designer_agent, request)


async def run_reviewer_agent(draft):
    """
    Return review comments for the draft study guide.
    """
    return await run_agent(reviewer_agent, draft)


# ---------- Markdown assembly ----------

def assemble_markdown(topic, explanation, practice):
    """
    Build the draft study guide (everything before the review).
    """
    return (
        f"# Topic\n\n{topic}\n\n"
        f"{explanation}\n\n"
        f"{practice}\n"
    )


def get_recommendation(review):
    """
    Return the reviewer's recommendation line, or a default text.
    """
    match = re.search(r"Recommendation:\**\s*(.+)", review)
    if match:
        return match.group(1).strip()
    return "No recommendation given."


def assemble_final_markdown(topic, draft, review):
    """
    Build the final guide: draft + review comments + final summary.
    """
    summary = (
        "## Final Summary\n\n"
        f"This study guide covers **{topic}**: a simple explanation, "
        "key concepts, an example, a practice exercise and common "
        "mistakes.\n\n"
        f"**Reviewer recommendation:** {get_recommendation(review)}\n"
    )
    return f"{draft}\n{review}\n\n{summary}"


# ---------- Workflow ----------

async def run_workflow(topic):
    """
    Run the agents in order and return the final Markdown guide.
    """
    print("[1/5] Explainer Agent: writing the explanation...")
    explanation = await run_explainer_agent(topic)

    print("[2/5] Practice Designer Agent: creating the exercise...")
    practice = await run_practice_designer_agent(topic, explanation)

    print("[3/5] Assembling the draft study guide...")
    draft = assemble_markdown(topic, explanation, practice)

    print("[4/5] Reviewer Agent: reviewing the draft...")
    review = await run_reviewer_agent(draft)

    print("[5/5] Assembling the final Markdown...")
    return assemble_final_markdown(topic, draft, review)


def main():
    """
    Check the input and configuration, run the workflow,
    validate and save the guide. Return the exit status.
    """
    try:
        topic = get_topic()
        print("Checking configuration...")
        config = check_config()
        print(f"Configuration OK (model: {config['MODEL_NAME']})\n")
    except (ValueError, ConfigError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    final_markdown = asyncio.run(run_workflow(topic))
    status = 0

    print("\nValidation Tool: checking required sections...")
    result = validate_required_sections(final_markdown)
    if result["valid"]:
        print("Validation: OK, all required sections are present.")
    else:
        print("Validation FAILED: missing sections -> "
              + ", ".join(result["missing"]), file=sys.stderr)
        print("The guide is still saved so you can inspect it. "
              "Try running the command again.", file=sys.stderr)
        status = 1

    print("Save Markdown Tool: writing the file...")
    file_path = f"{OUTPUT_DIR}/{topic_to_filename(topic)}"
    message = save_markdown_file(file_path, final_markdown)
    if message.startswith("Error"):
        print(message, file=sys.stderr)
        return 1
    print(message)
    return status


if __name__ == "__main__":
    sys.exit(main())
