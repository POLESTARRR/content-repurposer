# Daily Log

## 2026-08-27
`engine/extract.py`'s `extract_text()` falls back to a raw UTF-8 decode for any unrecognized file extension, so dropping in a binary file like `.pptx` or `.xlsx` would silently produce garbage text instead of a clear "unsupported format" error.

## 2026-09-02
`engine/limits.py`'s `CHAR_LIMITS` has no plain `youtube` or `newsletter` key (only `youtube_title`/`youtube_desc` and `newsletter_subject`/`newsletter_body`), and `app.py`'s `_char_limit_for()` maps those two platforms to the split keys explicitly while everything else falls through to `platform` directly via `.get()` with an effectively unlimited default -- deliberate, but easy to break silently if a new platform with split parts gets added later without updating that branch.


## 2026-09-05
In app.py, edits made in the platform text boxes are only shown in the UI and are not written back to st.session_state.results before export. So the ZIP and calendar downloads can contain older generated text instead of the user’s edited copy.
