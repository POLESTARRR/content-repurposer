"""Platform rules: character limits, hashtag caps, and general
best-time-to-post benchmarks (industry rules of thumb -- always beaten
by your own analytics once you have them)."""
from __future__ import annotations

PLATFORMS = ["x", "instagram", "facebook", "linkedin", "youtube", "tiktok", "newsletter"]

DISPLAY_NAME = {
    "x": "X (Twitter)",
    "instagram": "Instagram",
    "facebook": "Facebook",
    "linkedin": "LinkedIn",
    "youtube": "YouTube",
    "tiktok": "TikTok",
    "newsletter": "Newsletter",
}

# soft/ideal and hard limits, in characters (per single tweet for X)
CHAR_LIMITS = {
    "x": {"ideal": 240, "hard": 280},
    "instagram": {"ideal": 800, "hard": 2200},
    "facebook": {"ideal": 400, "hard": 63206},
    "linkedin": {"ideal": 1800, "hard": 3000},
    "youtube_title": {"ideal": 60, "hard": 100},
    "youtube_desc": {"ideal": 1500, "hard": 5000},
    "tiktok": {"ideal": 800, "hard": 2200},
    "newsletter_subject": {"ideal": 55, "hard": 78},
    "newsletter_body": {"ideal": 4500, "hard": 8000},
}

MAX_HASHTAGS = {
    "x": 0,
    "instagram": 5,
    "facebook": 1,
    "linkedin": 4,
    "youtube": 4,
    "tiktok": 5,
    "newsletter": 0,
}

BEST_TIMES = {
    "x": "Weekdays 8-10am or 12-1pm (catch commute + lunch scrolling)",
    "instagram": "Tue-Thu 10am-1pm, or evenings 7-9pm",
    "facebook": "Tue-Thu 1-3pm (afternoon slump scrolling)",
    "linkedin": "Tue-Thu 8-10am (before the workday starts)",
    "youtube": "Thu-Fri 2-4pm, or weekend mornings for leisure viewing",
    "tiktok": "Tue/Thu/Fri 6-9pm (evening scroll sessions)",
    "newsletter": "Tue or Thu mornings, 7-9am",
}

PLATFORM_RULES = {
    "x": "Sharp, opinionated, builder voice. Single tweet under 280 chars for hot takes, "
         "or a thread of 2-6 tweets for deeper content (separate tweets with '---' on its own line). "
         "No hashtags unless genuinely trending. First tweet IS the hook -- never bury it.",
    "instagram": "Short paragraphs with line breaks for breathing room. 600-800 characters. "
                 "2-5 relevant hashtags at the end. Last line is a clear CTA (comment a keyword, save, or check bio).",
    "facebook": "Conversational and personal -- Facebook rewards posts that spark comments over "
                "posts that just get likes. Shorter posts (under ~400 chars) outperform long ones. "
                "End with a genuine question to drive discussion. At most 1 hashtag (they don't help reach on FB).",
    "linkedin": "First line is the hook before the 'see more' cut -- it must earn the click. "
                "Personal story + concrete insight format. Professional but not corporate. "
                "1200-2000 characters. 3-5 professional hashtags at the end.",
    "youtube": "Title: specific, SEO-aware, under 60 chars, promises a clear takeaway, numbers/names beat abstractions. "
               "Description: first 2 lines are the hook (visible above the fold), 150-300 words, "
               "include search-relevant keywords, end with a CTA (subscribe/newsletter).",
    "tiktok": "Lowercase, conversational, hook in the first line. 600-800 characters. "
              "3-5 hashtags. Can overlap with Instagram caption but should lead with a stronger scroll-stop line.",
    "newsletter": "Smart-friend register, not corporate. 400-700 words. Personal asides welcome. "
                  "One specific, concrete takeaway in the closing line. Subject line under 60 chars.",
}
