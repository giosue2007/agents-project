#!/usr/bin/env python3
"""
Validation tool: checks that a Markdown study guide has every
required section heading.
"""
import re

REQUIRED_SECTIONS = [
    "Topic",
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Practice Exercise",
    "Common Mistakes",
    "Review Comments",
    "Final Summary",
]


def find_headings(markdown: str) -> set:
    """
    Return the lowercase text of every Markdown heading (#, ##, ###...).
    A trailing ':' is ignored, so '## Example:' counts as 'example'.
    """
    headings = set()
    for line in markdown.splitlines():
        match = re.match(r"^\s*#{1,6}\s+(.+?)\s*:?\s*$", line)
        if match:
            headings.add(match.group(1).strip().lower())
    return headings


def validate_required_sections(markdown: str) -> dict:
    """
    Check that each required section appears as a heading.
    Return {"valid": bool, "missing": [section, ...]}.
    """
    headings = find_headings(markdown)
    missing = [
        section for section in REQUIRED_SECTIONS
        if section.lower() not in headings
    ]
    return {"valid": not missing, "missing": missing}
