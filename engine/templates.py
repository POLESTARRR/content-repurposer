"""Zero-setup fallback engine: deterministic, template + extractive-summary
based content generation. No AI model required -- this is what runs the
instant you unzip the app, and what silently backstops any platform where
the local LLM call fails or isn't installed."""
from __future__ import annotations

from . import analysis

CTA = {
    "x": "Full breakdown below.",
    "instagram": "Save this for later. Drop a \U0001F449 if this hit home.",
    "facebook": "What's your take? Agree or disagree?",
    "linkedin": "Curious how others are approaching this. What's worked for you?",
    "youtube": "Subscribe for more breakdowns like this one.",
    "tiktok": "follow for more like this",
    "newsletter": "Reply and tell me which part resonated most.",
}


def _fit(text: str, limit: int) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return cut.rstrip(",.;:") + "…"


def _keyword(text: str) -> str:
    freqs = analysis.keyword_frequencies(text)
    if not freqs:
        return "this"
    word = freqs.most_common(1)[0][0]
    return word


def _hook_variants(keyword: str, lead: str) -> list[str]:
    kw = keyword[0].upper() + keyword[1:]
    variants = [
        f"{kw} is not what most people think.",
        f"3 things about {keyword} nobody tells you.",
        f"What if everything you knew about {keyword} was wrong?",
    ]
    if lead and 20 <= len(lead) <= 140:
        variants[0] = lead
    return variants


def _lower_hooks(hooks: list[str]) -> list[str]:
    return [h[0].lower() + h[1:] if h else h for h in hooks]


def generate(platform: str, source_text: str) -> dict:
    keyword = _keyword(source_text)
    sentences = analysis.top_sentences(source_text, n=8)
    lead = sentences[0] if sentences else ""
    body_sentences = sentences[1:] if len(sentences) > 1 else sentences
    hashtags_pool = analysis.extract_hashtags(source_text, max_tags=8)

    if platform == "x":
        return _gen_x(keyword, lead, body_sentences)
    if platform == "instagram":
        return _gen_instagram(keyword, lead, body_sentences, hashtags_pool)
    if platform == "facebook":
        return _gen_facebook(keyword, lead, body_sentences, hashtags_pool)
    if platform == "linkedin":
        return _gen_linkedin(keyword, lead, body_sentences, hashtags_pool)
    if platform == "youtube":
        return _gen_youtube(keyword, lead, body_sentences, hashtags_pool)
    if platform == "tiktok":
        return _gen_tiktok(keyword, lead, body_sentences, hashtags_pool)
    if platform == "newsletter":
        return _gen_newsletter(keyword, lead, body_sentences)
    raise ValueError(f"Unknown platform: {platform}")


def _gen_x(keyword, lead, body_sentences):
    hooks = _hook_variants(keyword, lead)
    tweets = [_fit(hooks[0], 270)]
    for s in body_sentences[:4]:
        tweets.append(_fit(s, 270))
    tweets.append(_fit(CTA["x"], 270))
    thread = [f"{i+1}/ {t}" if i > 0 else t for i, t in enumerate(tweets)]
    return {
        "hooks": hooks,
        "title": None,
        "body": "\n\n".join(thread),
        "hashtags": [],
        "engine": "template",
    }


def _gen_instagram(keyword, lead, body_sentences, hashtags_pool):
    hooks = _hook_variants(keyword, lead)
    body = " ".join(body_sentences[:3])
    caption = f"{hooks[0]}\n\n{_fit(body, 500)}\n\n{CTA['instagram']}"
    tags = hashtags_pool[:5]
    if tags:
        caption += "\n\n" + " ".join(tags)
    return {"hooks": hooks, "title": None, "body": _fit(caption, 2200), "hashtags": tags, "engine": "template"}


def _gen_facebook(keyword, lead, body_sentences, hashtags_pool):
    hooks = _hook_variants(keyword, lead)
    body = " ".join(body_sentences[:2])
    caption = f"{hooks[2]}\n\n{_fit(body, 280)}\n\n{CTA['facebook']}"
    tags = hashtags_pool[:1]
    if tags:
        caption += "\n\n" + tags[0]
    return {"hooks": hooks, "title": None, "body": _fit(caption, 63206), "hashtags": tags, "engine": "template"}


def _gen_linkedin(keyword, lead, body_sentences, hashtags_pool):
    hooks = _hook_variants(keyword, lead)
    story = "\n\n".join(body_sentences[:4]) if body_sentences else lead
    takeaway = f"The takeaway: {body_sentences[-1] if body_sentences else lead}"
    caption = f"{hooks[0]}\n\n{story}\n\n{takeaway}\n\n{CTA['linkedin']}"
    tags = hashtags_pool[:5]
    if tags:
        caption += "\n\n" + " ".join(tags)
    return {"hooks": hooks, "title": None, "body": _fit(caption, 3000), "hashtags": tags, "engine": "template"}


def _gen_youtube(keyword, lead, body_sentences, hashtags_pool):
    kw = keyword[0].upper() + keyword[1:]
    title = _fit(f"{kw}: What You're Getting Wrong", 60)
    hooks = _hook_variants(keyword, lead)
    desc_body = " ".join(body_sentences[:6])
    description = f"{hooks[0]}\n\n{_fit(desc_body, 900)}\n\n{CTA['youtube']}"
    tags = hashtags_pool[:4]
    if tags:
        description += "\n\n" + " ".join(tags)
    return {"hooks": hooks, "title": title, "body": _fit(description, 5000), "hashtags": tags, "engine": "template"}


def _gen_tiktok(keyword, lead, body_sentences, hashtags_pool):
    hooks = _lower_hooks(_hook_variants(keyword, lead))
    body = " ".join(body_sentences[:2]).lower()
    caption = f"{hooks[0]}\n\n{_fit(body, 500)}\n\n{CTA['tiktok']}"
    tags = hashtags_pool[:5]
    if tags:
        caption += "\n\n" + " ".join(t.lower() for t in tags)
    return {"hooks": hooks, "title": None, "body": _fit(caption, 2200), "hashtags": tags, "engine": "template"}


def _gen_newsletter(keyword, lead, body_sentences):
    kw = keyword[0].upper() + keyword[1:]
    subject = _fit(f"The truth about {keyword}", 60)
    intro = lead or f"Let's talk about {keyword}."
    body = "\n\n".join(body_sentences[:8])
    closing = f"{CTA['newsletter']}"
    full = f"{intro}\n\n{body}\n\n{closing}"
    return {"hooks": [subject], "title": subject, "body": _fit(full, 8000), "hashtags": [], "engine": "template"}
