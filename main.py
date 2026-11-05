#!/usr/bin/env python3
"""
Entry point: run the Explainer Agent on a topic.

Usage:
    python3 main.py "Python decorators"
"""
import asyncio
import re
import sys

from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.explainer_agent import explainer_agent
from tools.file_writer import save_markdown_file

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


def main():
    """
    Read the topic from the command line (or ask for it), print
    the agent's explanation and save it as Markdown in output/.
    """
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Topic: ").strip()

    if not topic:
        print("Usage: python3 main.py \"<topic>\"")
        sys.exit(1)

    answer = asyncio.run(run_agent(explainer_agent, topic))
    print(answer)

    file_path = f"{OUTPUT_DIR}/{topic_to_filename(topic)}"
    print(save_markdown_file(file_path, answer))


if __name__ == "__main__":
    main()
