#!/usr/bin/env python3
"""
Explainer Agent: explains a programming topic for beginner students.
"""
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/llama3.2:1b")

INSTRUCTION = """You are a patient teacher for beginner programming students.
The user gives you a topic.
Answer in Markdown with exactly these three sections:

## Simple Explanation
Two or three short sentences explaining the topic in simple words.

## Key Concepts
A bullet list of 3 to 5 key concepts, one short line each.

## Example
One simple example. If it is code, put it in a code block.

Do not add any other section. Keep the whole answer short."""

explainer_agent = Agent(
    name="explainer_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Explains a topic with key concepts and an example.",
    instruction=INSTRUCTION,
)
