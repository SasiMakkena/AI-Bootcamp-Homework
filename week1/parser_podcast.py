"""
Podcast parser: safely extract YAML frontmatter, normalize fields, and return records.
"""

from pathlib import Path
from typing import Tuple, Dict, Any
import yaml
from github_reader import RawRepositoryFile


def safe_parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """
    Extract YAML frontmatter (if present) and the remaining body.
    Returns (meta_dict, body_text). Robust to missing/invalid YAML.
    """
    text = (text or "").lstrip()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) > 2:
            yaml_part = parts[1]
            body_part = parts[2].strip()
            try:
                meta = yaml.safe_load(yaml_part) or {}
            except Exception:
                meta = {}
                body_part = text
            return meta, body_part
    return {}, text.strip()


def parse_podcast_raw(raw_file: RawRepositoryFile) -> Dict[str, Any]:
    """
    Convert a RawRepositoryFile into a normalized podcast record.
    Handles files with or without transcript/frontmatter.
    """
    meta, body = safe_parse_frontmatter(raw_file.content or "")
    return {
        "filename": raw_file.filename,
        "title": meta.get("title") or Path(raw_file.filename).stem,
        "season": meta.get("season"),
        "episode": meta.get("episode"),
        "guests": meta.get("guests") or meta.get("guest") or [],
        "links": meta.get("links") or {},
        "ids": meta.get("ids") or {},
        "transcript": meta.get("transcript") or [],
        "body": body,
    }
