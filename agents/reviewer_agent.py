#!/usr/bin/env python3
"""
Reviewer Agent: reviews a draft study guide and comments on it,
without rewriting it.
"""
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/llama3.2:1b")

INSTRUCTION = """You are a reviewer agent.
You receive a draft study guide for beginner programming students.
Review it for clarity, completeness, correctness and usefulness.
Be critical but constructive. Be specific: point to the exact part
that has a problem (for example "the expected output of the exercise
does not match the input list").
Do not rewrite the guide.

Answer in Markdown with exactly this structure:

## Review Comments

**Missing information:**
- One short point per line, or "None".

**Unclear parts:**
- One short point per line, or "None".

**Suggestions:**
- One short, actionable suggestion per line.

**Recommendation:** APPROVED or NEEDS REVISION, followed by one
short sentence explaining why.

Return only this section. Keep it short."""

reviewer_agent = Agent(
    name="reviewer_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Reviews a draft study guide and gives short comments.",
    instruction=INSTRUCTION,
)
