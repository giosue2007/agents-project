#!/usr/bin/env python3
"""
Entry point: run the Explainer Agent on a topic.

Usage:
    python3 main.py "Python decorators"
"""
import asyncio
import sys

from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.explainer_agent import explainer_agent

APP_NAME = "agents_project"
USER_ID = "student"


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
    Read the topic from the command line (or ask for it) and print
    the agent's explanation.
    """
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Topic: ").strip()

    if not topic:
        print("Usage: python3 main.py \"<topic>\"")
        sys.exit(1)

    print(asyncio.run(run_agent(explainer_agent, topic)))


if __name__ == "__main__":
    main()
