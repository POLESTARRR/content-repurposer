# Recast

Turn one piece of writing (a blog post, article, or script) into
platform-native posts for **X, Instagram, Facebook, LinkedIn, YouTube,
TikTok, and your newsletter**, ready to publish, with hooks scored,
hashtags suggested, and a posting calendar built for you.

**$0 to run, forever, on any of its three engines.** The default needs no
signup and no API key at all; the two AI engines are both free but do
require a one-time, no-cost setup step.

## How it generates content

Recast has three engines and picks the best one available automatically.

1. **Local AI (optional, better quality).** If you have [Ollama](https://ollama.com)
   installed, Recast uses whatever model you've pulled to write richer,
   more natural platform variants. Ollama runs entirely on your own Mac,
   so nothing is sent over the internet, there's no account, and there's
   no per-use cost.
2. **Gemini, free tier (optional, better quality, zero install).** If you'd
   rather not install anything locally, a free [Google AI Studio](https://aistudio.google.com/apikey)
   key gets you the same richer, more natural writing via the cloud instead.
   Requires a one-time signup for the key; nothing else changes.
3. **Instant template engine (zero setup).** If neither AI engine is
   configured, Recast falls back automatically to a built-in rule-based
   generator (extractive summarization plus platform templates). It works
   the moment you open the app, with no installation or signup at all.

Either way you get three scored hook options, a full post, suggested
hashtags, a character-limit check against that platform's real rules,
and a best-time-to-post suggestion for every platform you select.

## Quick start

1. Double-click **`Run Recast.command`**.
   - The first run installs a small local Python environment and a few
     libraries (Streamlit, python-docx, pypdf). It takes about a minute.
   - Your browser opens the app automatically.
2. Click **"Load sample"** to try it instantly, or upload or paste your
   own writing (`.txt`, `.md`, `.pdf`, `.docx` all work).
3. Click **Repurpose content**.
4. Edit anything inline, then download the full bundle (all platforms as
   markdown, plus a `content_calendar.csv` for scheduling) or grab
   individual posts. Every run is also saved automatically under `output/`.

## Want richer AI written output? (optional, still free)

Two options, pick either:

**Local, offline:**
```bash
brew install ollama
ollama pull llama3.2:3b
```

**Cloud, free tier:** get a free key from [Google AI Studio](https://aistudio.google.com/apikey),
then create `.streamlit/secrets.toml` (see `.streamlit/secrets.toml.example`)
with:
```toml
GEMINI_API_KEY = "your-key-here"
```

Reload the app either way. The sidebar will show which engine is active
("Local AI · llama3.2:3b" or "Gemini") and generations route through it
automatically, with no further setup. Ollama is tried first if both are
configured, since it keeps everything on your own machine.

## Make it sound like you

Open the **"Your voice"** section in the sidebar and fill in `voice.md`
with a few lines that have worked for you before, openers and closers
you like, and phrases you never want to see (corporate filler, AI-isms,
and so on). Every generation run is checked against your banned-phrase
list afterward, and you'll get a warning if anything slipped through,
whichever engine wrote it.

## Project layout

```
Content Repurposer/
  app.py                  Streamlit app (the UI)
  theme.py                 the monochrome graphite-on-paper theme
  engine/
    extract.py               reads .txt/.md/.pdf/.docx into plain text
    ollama_client.py          talks to a local Ollama model, if present
    gemini_client.py           talks to Gemini's free tier, if configured
    templates.py               zero setup rule-based fallback generator
    generator.py               hybrid orchestrator, voice and banned-phrase lint
    analysis.py                 hook scoring, hashtag and keyword extraction
    limits.py                    per-platform char limits and best-time data
    export.py                    writes output bundles and the calendar CSV
  voice.md                  your voice notes (edit via the sidebar too)
  sample_input.md            example article for a quick test run
  output/                   every run is saved here, timestamped
  requirements.txt
  Run Recast.command       double-click launcher
```

## Notes

- Best-time-to-post times are general industry benchmarks, not your
  personal analytics. Once you have your own engagement data, trust
  that over this cheat sheet.
- The hook score is a heuristic (numbers, questions, generic-opener
  detection, length), not a guarantee of virality. Treat it as a
  second opinion, not a verdict.
