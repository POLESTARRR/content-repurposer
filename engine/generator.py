"""Hybrid orchestrator: tries the local Ollama model for each platform,
falls back to the deterministic template engine per-platform on any
failure, and always runs a deterministic voice/banned-phrase lint pass
(that part never depends on AI being available at all)."""
from __future__ import annotations

import re

from . import analysis, limits, ollama_client, templates

HARD_RULES = """HARD RULES (never violate):
- No em dashes or double dashes
- Never open with "Here's the X you requested" or similar
- Never close with "Let me know if anything else"
- Every output must contain one specific, concrete takeaway
- Never just copy the source verbatim"""

_STRUCT_RE = re.compile(
    r"HOOK1:\s*(?P<h1>.*?)\s*\n"
    r"HOOK2:\s*(?P<h2>.*?)\s*\n"
    r"HOOK3:\s*(?P<h3>.*?)\s*\n"
    r"(?:TITLE:\s*(?P<title>.*?)\s*\n)?"
    r"BODY:\s*\n(?P<body>.*?)\n"
    r"HASHTAGS:\s*(?P<tags>.*)",
    re.DOTALL,
)


def _build_prompt(platform: str, source_text: str, voice_text: str) -> str:
    voice_block = voice_text.strip() if voice_text and voice_text.strip() else (
        "(no voice notes provided -- use a clear, confident, non-corporate voice)"
    )
    shared = (
        "You are repurposing one piece of source content into a platform-native "
        "social media post. Preserve the author's voice.\n\n"
        f"SOURCE CONTENT:\n{source_text[:3000]}\n\n"
        f"VOICE NOTES (match this tone; never use anything listed as banned):\n{voice_block[:1000]}\n\n"
        f"{HARD_RULES}\n"
    )
    thread_note = (
        "\nIf writing an X thread, number each tweet after the first like "
        "'2/ ...' and separate tweets with a blank line. Never use em dashes "
        "or a row of dashes as a separator.\n" if platform == "x" else ""
    )
    return (
        f"{shared}\n"
        f"PLATFORM: {limits.DISPLAY_NAME[platform]}\n"
        f"{limits.PLATFORM_RULES[platform]}\n"
        f"{thread_note}\n"
        "Respond in EXACTLY this format and nothing else, no preamble:\n"
        "HOOK1: <first hook option, one line>\n"
        "HOOK2: <second hook option, one line>\n"
        "HOOK3: <third hook option, one line>\n"
        + ("TITLE: <video title, one line>\n" if platform == "youtube" else "")
        + "BODY:\n<the full post text, can be multiple lines>\n"
        "HASHTAGS: <space-separated hashtags, or NONE>"
    )


def _parse_structured(raw: str) -> dict | None:
    m = _STRUCT_RE.search(raw)
    if not m:
        return None
    body = m.group("body").strip()
    if not body:
        return None
    tags_raw = m.group("tags").strip()
    tags = [] if tags_raw.upper() == "NONE" else [t for t in tags_raw.split() if t.startswith("#")]
    return {
        "hooks": [m.group("h1").strip(), m.group("h2").strip(), m.group("h3").strip()],
        "title": (m.group("title") or "").strip() or None,
        "body": body,
        "hashtags": tags,
        "engine": "ollama",
    }


# token budget per platform -- just enough for hooks + body + hashtags, capped
# tightly so a single call can't run away and dominate the whole batch's time
NUM_PREDICT = {
    "x": 350, "instagram": 350, "facebook": 250, "linkedin": 550,
    "youtube": 400, "tiktok": 300, "newsletter": 750,
}


def generate_one(platform: str, source_text: str, voice_text: str, use_ai: bool, model: str | None) -> dict:
    if use_ai and ollama_client.is_available():
        prompt = _build_prompt(platform, source_text, voice_text)
        raw = ollama_client.generate(prompt, model=model, num_predict=NUM_PREDICT.get(platform, 400))
        if raw:
            parsed = _parse_structured(raw)
            if parsed:
                return parsed
    # fallback: deterministic template engine (always works, zero setup)
    return templates.generate(platform, source_text)


def run(platforms: list[str], source_text: str, voice_text: str, use_ai: bool = True, on_progress=None) -> dict:
    """on_progress, if given, is called as on_progress(platform, result) right after
    each platform finishes -- lets the UI show live progress instead of one long
    silent wait for the whole batch."""
    model = ollama_client.default_model() if use_ai else None
    results = {}
    for platform in platforms:
        result = generate_one(platform, source_text, voice_text, use_ai, model)
        result["hook_scores"] = [analysis.score_hook(h) for h in result["hooks"]]
        results[platform] = result
        if on_progress:
            on_progress(platform, result)
    results["_meta"] = {
        "ai_available": ollama_client.is_available() if use_ai else False,
        "model": model,
    }
    return results


def lint_against_voice(results: dict, voice_text: str) -> dict:
    banned = _extract_banned_phrases(voice_text)
    if not banned:
        return {}
    hits = {}
    for platform, result in results.items():
        if platform == "_meta":
            continue
        text = result.get("body", "") + " ".join(result.get("hooks", []))
        found = analysis.banned_phrases_found(text, banned)
        if found:
            hits[platform] = found
    return hits


def _extract_banned_phrases(voice_text: str) -> list[str]:
    if not voice_text:
        return []
    m = re.search(r"##+\s*Banned phrases(.*?)(\n##|\Z)", voice_text, re.IGNORECASE | re.DOTALL)
    if not m:
        return []
    section = m.group(1)
    phrases = []
    for line in section.splitlines():
        line = line.strip().lstrip("-*").strip().strip('"')
        if line:
            phrases.append(line)
    return phrases
