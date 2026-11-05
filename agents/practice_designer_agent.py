#!/usr/bin/env python3
"""
Practice Designer Agent: creates a small exercise from a topic
and the explanation written by the Explainer Agent.
"""
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/llama3.2:1b")

INSTRUCTION = """You are a practice designer agent.
You receive a topic and an explanation of that topic.
Create one short beginner-friendly exercise based on them.
The exercise must take 10 to 20 minutes and need no external service.
Do not rewrite the explanation.

Answer in Markdown with exactly this structure:

## Practice Exercise
One or two sentences describing what the student must do.

**Expected input:** the input, or "None" if not applicable.

**Expected output:** the expected result, or "None" if not applicable.

**Hints:**
- First hint.
- Second hint (optional).

## Common Mistakes
- Two or three mistakes beginners often make with this topic,
  one short line each.

Return only these two sections."""

practice_designer_agent = Agent(
    name="practice_designer_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Creates a small exercise and lists common mistakes.",
    instruction=INSTRUCTION,
)
