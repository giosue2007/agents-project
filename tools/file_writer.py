#!/usr/bin/env python3
"""
File writer tool: saves Markdown content to disk.
"""
from pathlib import Path


def save_markdown_file(file_path: str, content: str) -> str:
    """
    Write content to file_path, creating parent directories if needed.
    Return a success message with the saved path, or an error message.
    """
    path = Path(file_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except OSError as error:
        return f"Error: could not save {path}: {error}"
    return f"Saved to {path}"
