"""Zero-dependency text analysis: sentence splitting, keyword/hashtag
extraction, extractive summarization, and hook-strength scoring.

Everything here is plain-Python heuristics -- no ML model, no API call --
so it runs instantly and is also what powers the no-setup template
fallback engine.
"""
from __future__ import annotations

import re
from collections import Counter

STOPWORDS = set("""
a about above after again against all am an and any are aren't as at be
because been before being below between both but by can't cannot could
couldn't did didn't do does doesn't doing don't down during each few for
from further had hadn't has hasn't have haven't having he he'd he'll he's
her here here's hers herself him himself his how how's i i'd i'll i'm i've
if in into is isn't it it's its itself let's me more most mustn't my myself
no nor not of off on once only or other ought our ours ourselves out over
own same shan't she she'd she'll she's should shouldn't so some such than
that that's the their theirs them themselves then there there's these they
they'd they'll they're they've this those through to too under until up
very was wasn't we we'd we'll we're we've were weren't what what's when
when's where where's which while who who's whom why why's with won't would
wouldn't you you'd you'll you're you've your yours yourself yourselves
also just like get got make made really very much many one two use used
using new
""".split())

POWER_WORDS = {
    "secret", "proven", "mistake", "mistakes", "stop", "never", "always",
    "free", "surprising", "truth", "warning", "nobody", "everyone", "actually",
    "wrong", "right", "best", "worst", "fast", "instantly", "simple", "easy",
    "hard", "hidden", "unknown", "science", "data", "study", "before", "after",
    "why", "how", "what", "this", "you", "your",
}

GENERIC_OPENERS = [
    "in today's fast-paced world", "in this article", "in this post",
    "in this blog", "have you ever wondered", "let me tell you",
    "in this day and age", "as we all know", "without further ado",
]

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]{2,}")


def split_sentences(text: str) -> list[str]:
    """Split into sentences, treating blank-line paragraph breaks (and
    markdown headings/list markers, which never end in punctuation) as
    hard boundaries -- otherwise a heading like "# My Title" silently
    glues onto the next paragraph's first sentence."""
    if not text or not text.strip():
        return []

    sentences = []
    for para in re.split(r"\n\s*\n", text.strip()):
        para = re.sub(r"^#{1,6}\s*", "", para.strip())
        para = re.sub(r"^[-*]\s+", "", para)
        para = re.sub(r"^\d+[.)]\s+", "", para)
        para = re.sub(r"\s+", " ", para).strip()
        if not para:
            continue
        for part in SENTENCE_SPLIT_RE.split(para):
            part = part.strip()
            if part:
                sentences.append(part)
    return sentences


def keyword_frequencies(text: str) -> Counter:
    words = [w.lower() for w in WORD_RE.findall(text)]
    words = [w for w in words if w not in STOPWORDS and len(w) > 3]
    return Counter(words)


def extract_hashtags(text: str, max_tags: int = 6) -> list[str]:
    freqs = keyword_frequencies(text)
    top = [w for w, _ in freqs.most_common(max_tags * 2)]
    tags = []
    for w in top:
        tag = "#" + w[0].upper() + w[1:]
        if tag not in tags:
            tags.append(tag)
        if len(tags) >= max_tags:
            break
    return tags


def top_sentences(text: str, n: int = 5) -> list[str]:
    """Cheap Luhn-style extractive summary: score sentences by density
    of high-frequency keywords, keep original order."""
    sentences = split_sentences(text)
    if len(sentences) <= n:
        return sentences

    freqs = keyword_frequencies(text)
    if not freqs:
        return sentences[:n]

    scored = []
    for idx, sent in enumerate(sentences):
        words = [w.lower() for w in WORD_RE.findall(sent)]
        if not words:
            continue
        score = sum(freqs.get(w, 0) for w in words) / len(words)
        # small boost for early sentences (hooks/intros tend to matter)
        if idx == 0:
            score *= 1.3
        scored.append((score, idx, sent))

    scored.sort(key=lambda t: t[0], reverse=True)
    chosen = sorted(scored[:n], key=lambda t: t[1])
    return [s for _, _, s in chosen]


def score_hook(hook: str) -> dict:
    """Heuristic 0-100 hook-strength score with human-readable notes."""
    text = hook.strip()
    lower = text.lower()
    score = 50
    notes = []

    if not text:
        return {"score": 0, "notes": ["Empty hook."]}

    if re.match(r"^\d", text) or re.search(r"\b\d+\b", text[:40]):
        score += 12
        notes.append("+ Leads with a number/stat -- concrete beats abstract.")

    if text.rstrip().endswith("?"):
        score += 8
        notes.append("+ Question hook -- invites a reply.")

    hit_power = [w for w in POWER_WORDS if re.search(rf"\b{re.escape(w)}\b", lower)]
    if hit_power:
        score += min(15, 5 * len(hit_power))
        notes.append(f"+ Uses attention words: {', '.join(sorted(hit_power)[:3])}.")

    for opener in GENERIC_OPENERS:
        if lower.startswith(opener):
            score -= 25
            notes.append(f"- Starts with an overused opener (\"{opener}\").")
            break

    length = len(text)
    if length > 120:
        score -= 12
        notes.append("- Hook is long; punchier openers get more scroll-stops.")
    elif length < 15:
        score -= 8
        notes.append("- Hook may be too short to create curiosity.")
    else:
        notes.append("+ Good length for a scroll-stopping first line.")

    if any(text.startswith(w) for w in ("Here's", "Here is", "Let me")):
        score -= 8
        notes.append("- \"Here's/Let me\" openings read as generic AI-speak.")

    score = max(0, min(100, score))
    return {"score": score, "notes": notes}


def banned_phrases_found(text: str, banned: list[str]) -> list[str]:
    lower = text.lower()
    return [p for p in banned if p.strip() and p.strip().lower() in lower]
