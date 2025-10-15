"""
Chunking utilities:
- extract_text_blocks(): transcript lines or markdown paragraphs
- sliding_window(): overlapping windows
- format_chunks(): add metadata to each chunk
- process_podcast_file(): end-to-end for one file
"""
from typing import List, Dict, Any


def extract_text_blocks(record: Dict[str, Any]) -> List[str]:
    """Return list of text blocks from transcript or markdown body."""
    transcript = record.get("transcript", [])
    if transcript and isinstance(transcript, list):
        # Use structured transcript lines
        return [t["line"].strip() for t in transcript if isinstance(t, dict) and "line" in t]
    # Otherwise, split markdown body into paragraphs
    body = record.get("body", "")
    return [p.strip() for p in body.split("\n\n") if p.strip()]


def sliding_window(seq: List[str], size: int = 30, overlap: int = 15) -> List[List[str]]:
    """Create overlapping chunks of text blocks."""
    if size <= 0 or overlap >= size:
        raise ValueError("size must be > 0 and overlap < size")

    chunks: List[List[str]] = []
    step = size - overlap

    for i in range(0, len(seq), step):
        window = seq[i:i + size]
        if window:
            chunks.append(window)
        if i + size >= len(seq):
            break

    return chunks


def format_chunks(record: Dict[str, Any], blocks: List[str],
                  size: int = 30, overlap: int = 15) -> List[Dict[str, Any]]:
    """Combine text blocks into overlapping chunks with metadata."""
    windows = sliding_window(blocks, size, overlap)
    formatted: List[Dict[str, Any]] = []
    for idx, window in enumerate(windows, 1):
        chunk_text = " ".join(window)
        formatted.append({
            "episode_title": record.get("title"),
            "filename": record.get("filename"),
            "season": record.get("season"),
            "episode": record.get("episode"),
            "chunk_id": idx,
            "text": chunk_text.strip(),
            "youtube": record.get("links", {}).get("youtube"),
        })
    return formatted


def process_podcast_file(raw_file, size: int = 30, overlap: int = 15) -> List[Dict[str, Any]]:
    """Parse one podcast markdown, extract blocks, and create chunks."""
    from parser_podcast import parse_podcast_raw  # local import to avoid cycles
    record = parse_podcast_raw(raw_file)
    blocks = extract_text_blocks(record)
    if not blocks:
        return []
    return format_chunks(record, blocks, size=size, overlap=overlap)
