#!/usr/bin/env python3
"""
Entry point: build a study guide for a topic with two agents.

Usage:
    python3 main.py "Python decorators"
"""
import asyncio
import re
import sys

from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.explainer_agent import explainer_agent
from agents.practice_designer_agent import practice_designer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections

APP_NAME = "agents_project"
USER_ID = "student"
OUTPUT_DIR = "output"


def topic_to_filename(topic):
    """
    Turn a topic into a safe file name, e.g. 'Python decorators'
    becomes 'python_decorators.md'.
    """
    name = re.sub(r"[^a-z0-9]+", "_", topic.lower()).strip("_")
    return (name or "explanation") + ".md"


async def run_agent(agent, text):
    """
    Send text to the agent and return its final answer as a string.
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
    return answer


async def build_study_guide(topic):
    """
    Run the Explainer Agent, then give its explanation to the
    Practice Designer Agent, and return the full Markdown guide.
    """
    explanation = await run_agent(explainer_agent, topic)

    practice_request = (
        f"Topic: {topic}\n\n"
        f"Explanation:\n{explanation}"
    )
    practice = await run_agent(practice_designer_agent, practice_request)

    return (
        f"# Study Guide\n\n## Topic\n\n{topic}\n\n"
        f"{explanation}\n\n{practice}\n"
    )


def main():
    """
    Read the topic from the command line (or ask for it), build the
    study guide, print it, save it in output/ and validate it.
    """
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Topic: ").strip()

    if not topic:
        print("Usage: python3 main.py \"<topic>\"")
        sys.exit(1)

    markdown = asyncio.run(build_study_guide(topic))
    print(markdown)

    file_path = f"{OUTPUT_DIR}/{topic_to_filename(topic)}"
    print(save_markdown_file(file_path, markdown))

    result = validate_required_sections(markdown)
    if result["valid"]:
        print("Validation: OK, all required sections are present.")
    else:
        print("Validation: missing sections -> "
              + ", ".join(result["missing"]))


if __name__ == "__main__":
    main()
