# Daily Log

## 2026-08-27
`engine/extract.py`'s `extract_text()` falls back to a raw UTF-8 decode for any unrecognized file extension, so dropping in a binary file like `.pptx` or `.xlsx` would silently produce garbage text instead of a clear "unsupported format" error.

## 2026-09-02
`engine/limits.py`'s `CHAR_LIMITS` has no plain `youtube` or `newsletter` key (only `youtube_title`/`youtube_desc` and `newsletter_subject`/`newsletter_body`), and `app.py`'s `_char_limit_for()` maps those two platforms to the split keys explicitly while everything else falls through to `platform` directly via `.get()` with an effectively unlimited default -- deliberate, but easy to break silently if a new platform with split parts gets added later without updating that branch.


## 2026-09-05
In app.py, edits made in the platform text boxes are only shown in the UI and are not written back to st.session_state.results before export. So the ZIP and calendar downloads can contain older generated text instead of the user’s edited copy.

## 2026-09-06
In app.py, edits made in the platform text boxes are only shown in the UI and are not written back to st.session_state.results before export. So the ZIP and calendar downloads can contain older generated text instead of the user's edited copy.

## 2026-09-07
In app.py, edits made in the platform text boxes are only shown in the UI and are not written back to st.session_state.results before export. So the ZIP and calendar downloads can contain older generated text instead of the user’s edited copy.

## 2026-10-12
The `count_tokens()` utility in `gemini_client.py` provides pre-flight token budget checks before API calls.

## 2026-10-12
The engine uses platform character limits to enforce hard truncation: Twitter at a specific limit, LinkedIn and Instagram at their respective maximums.

## 2026-10-12
The `_post_process()` method in `generator.py` truncates content to platform-specific character limits and only appends hashtags if they fit within the budget.

## 2026-10-19
The `gemini_client.py` wrapper uses `gemini-1.5-flash` model with hardcoded temperature=0.7 and top_p=0.9 parameters.

## 2026-10-19
Content generation prompts are assembled from platform-specific style instructions stored in the `PLATFORM_CONFIGS` dict.

## 2026-10-20
A `_safe_parse()` method in `gemini_client.py` strips markdown code fences (```json) from Gemini responses to handle structured output.

## 2026-10-22
No validation exists for empty or None responses from the Gemini API before attempting to parse them.

## 2026-10-22
Retry logic in `generator.py` is implemented via a `@retry(max_attempts=3, backoff=2)` decorator pattern with exponential backoff.

## 2026-10-23
The `DAILY_LOG.md` format uses date headers with nested bullet lists for content sources and platform-specific posting status.

## 2026-10-23
The retry decorator wraps the `generate_content()` method, making API failures resilient with automatic exponential backoff.

## 2026-10-23
Hashtags are generated as part of the `ContentPiece` dataclass and stored separately from the main text field.

## 2026-10-28
The `DAILY_LOG.md` tracks content sources, target platforms, generation status, and posting status in a structured markdown format.

## 2026-10-28
API key is loaded from environment variable `GEMINI_API_KEY` in `gemini_client.py` without fallback or validation.

## 2026-10-29
The `generator.py` uses a `ContentPiece` dataclass with fields for platform, text, hashtags, and char_count, providing structured content output.

## 2026-10-29
API key is loaded from environment variable `GEMINI_API_KEY` in `gemini_client.py` without fallback or validation.
