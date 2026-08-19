"""Thin wrapper around a locally-running Ollama instance.

Ollama (https://ollama.com) runs open-weight LLMs entirely on your own
machine -- no API key, no signup, no per-token cost, no data leaving
your laptop. This module never talks to any paid/cloud API. If Ollama
isn't installed or isn't running, `is_available()` returns False and
the rest of the app falls back to the template engine instead.
"""
from __future__ import annotations

import requests

BASE_URL = "http://localhost:11434"
TIMEOUT_HEALTH = 1.5
TIMEOUT_GENERATE = 300  # local models on modest hardware can be slow, especially on a cold load

PREFERRED_MODELS = [
    "llama3.2", "llama3.2:3b", "llama3.1", "llama3",
    "mistral", "gemma2", "phi3", "qwen2.5",
]


def is_available() -> bool:
    try:
        r = requests.get(f"{BASE_URL}/api/tags", timeout=TIMEOUT_HEALTH)
        return r.status_code == 200
    except requests.RequestException:
        return False


def list_models() -> list[str]:
    try:
        r = requests.get(f"{BASE_URL}/api/tags", timeout=TIMEOUT_HEALTH)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except requests.RequestException:
        return []


def default_model() -> str | None:
    models = list_models()
    if not models:
        return None
    for preferred in PREFERRED_MODELS:
        for m in models:
            if m == preferred or m.startswith(preferred + ":") or m.split(":")[0] == preferred:
                return m
    return models[0]


def generate(prompt: str, model: str | None = None, temperature: float = 0.7, num_predict: int = 400) -> str | None:
    """Run one generation. Returns None on any failure so callers can fall back cleanly.

    num_predict caps how many tokens the model may generate -- on modest hardware,
    an uncapped response is the single biggest driver of slow, unpredictable latency.
    """
    model = model or default_model()
    if not model:
        return None
    try:
        r = requests.post(
            f"{BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature, "num_predict": num_predict},
            },
            timeout=TIMEOUT_GENERATE,
        )
        r.raise_for_status()
        return r.json().get("response", "").strip() or None
    except requests.RequestException:
        return None
