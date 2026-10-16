"""Separate UI-only mode from heavyweight live RAG startup."""
from __future__ import annotations
from collections.abc import Callable
from typing import Any


def prepare_index(live_mode: bool, index_loader: Callable[[str], tuple[Any, int]], db_path: str):
    """In design-preview mode, never call the embedding/index loader."""
    if not live_mode:
        return None, 0, None
    try:
        index, count = index_loader(db_path)
        return index, count, None
    except Exception as error:
        return None, 0, f"{type(error).__name__}: {error}"
