# Daily Log

## 2026-08-27
`engine/extract.py`'s `extract_text()` falls back to a raw UTF-8 decode for any unrecognized file extension, so dropping in a binary file like `.pptx` or `.xlsx` would silently produce garbage text instead of a clear "unsupported format" error.

