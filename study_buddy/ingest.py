# study_buddy/ingest.py — WHY: turns markdown notes into citable chunks.
# Assessment topic 7 (RAG / chunking): split by heading first (topic boundaries), then by size
# with overlap (so a sentence cut at a boundary still appears whole in one chunk). Every chunk
# keeps metadata (source, heading, chunk_id) so answers can cite `source#heading`.
"""Load markdown files and split them into chunks with metadata."""

import re
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def load_markdown(folder: Path) -> list[tuple[str, str]]:
    """Return (source_filename, text) for every .md file, sorted for determinism."""
    return [(p.name, p.read_text(encoding="utf-8")) for p in sorted(folder.glob("*.md"))]


def split_by_heading(text: str) -> list[tuple[str, str]]:
    """Split markdown into (heading, body) sections. Header comments are dropped."""
    text = HTML_COMMENT_RE.sub("", text)
    sections: list[tuple[str, list[str]]] = [("(intro)", [])]
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            sections.append((match.group(2).strip(), []))
        else:
            sections[-1][1].append(line)
    return [(h, "\n".join(body).strip()) for h, body in sections if "\n".join(body).strip()]


def split_by_size(words: list[str], chunk_size: int, overlap: int) -> list[list[str]]:
    """Sliding window over words: windows of `chunk_size`, sharing `overlap` words."""
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("need chunk_size > 0 and 0 <= overlap < chunk_size")
    step = chunk_size - overlap
    windows = []
    for start in range(0, len(words), step):
        windows.append(words[start : start + chunk_size])
        if start + chunk_size >= len(words):
            break
    return windows


def chunk_document(source: str, text: str, chunk_size: int = 120, overlap: int = 20) -> list[dict]:
    """Chunk one document. chunk_id = '<file stem>-<nn>' (stable, human-readable)."""
    chunks = []
    stem = Path(source).stem
    for heading, body in split_by_heading(text):
        for window in split_by_size(body.split(), chunk_size, overlap):
            chunks.append(
                {
                    "chunk_id": f"{stem}-{len(chunks):02d}",
                    "source": source,
                    "heading": heading,
                    "text": " ".join(window),
                }
            )
    return chunks


def chunk_folder(folder: Path, chunk_size: int = 120, overlap: int = 20) -> list[dict]:
    """Chunk every markdown file in `folder`."""
    chunks = []
    for source, text in load_markdown(folder):
        chunks.extend(chunk_document(source, text, chunk_size, overlap))
    return chunks
