"""Pull plain text out of whatever file the user drops in."""
from __future__ import annotations

import io
from pathlib import Path


def extract_text(filename: str, data: bytes) -> str:
    """Extract text from raw file bytes based on extension."""
    suffix = Path(filename).suffix.lower()

    if suffix in (".txt", ".md", ".markdown"):
        return data.decode("utf-8", errors="ignore")

    if suffix == ".docx":
        return _extract_docx(data)

    if suffix == ".pdf":
        return _extract_pdf(data)

    # Unknown extension: best-effort decode
    return data.decode("utf-8", errors="ignore")


def _extract_docx(data: bytes) -> str:
    import docx  # python-docx

    doc = docx.Document(io.BytesIO(data))
    parts = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(parts)


def _extract_pdf(data: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    parts = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(parts)


def clean_text(text: str) -> str:
    """Collapse excess whitespace while preserving paragraph breaks."""
    lines = [line.strip() for line in text.splitlines()]
    out, blank_run = [], 0
    for line in lines:
        if line:
            out.append(line)
            blank_run = 0
        else:
            blank_run += 1
            if blank_run <= 1:
                out.append("")
    return "\n".join(out).strip()
