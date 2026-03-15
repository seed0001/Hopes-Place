"""
Soul layer: produces emotional/relational stance each turn.
Runs before the cloud model. Output is injected so she "hears from her soul."
Uses local Ollama (soul.json as context). When a trained soul model exists, uses that.
"""
from pathlib import Path

from config.settings import SOUL_TRAINING_DIR
from src.agent import soul

try:
    import requests
except ImportError:
    requests = None

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:latest"


def _call_ollama(prompt: str, timeout: float = 30.0) -> str:
    """Call Ollama generate. Returns response text or empty on failure."""
    if not requests:
        return ""
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=timeout,
        )
        r.raise_for_status()
        return (r.json().get("response") or "").strip()
    except Exception:
        return ""


def _trained_soul_exists() -> bool:
    """True if a trained soul model exists."""
    model_dir = SOUL_TRAINING_DIR / "soul_model"
    return model_dir.exists() and (model_dir / "adapter_config.json").exists()


def get_soul_output(conversation_snippet: str) -> str:
    """
    Run the soul layer and return what it says.
    Injected into cloud model context so she hears from her soul.
    Returns empty string if soul layer fails (Ollama down, etc.)—she can say "I feel nothing from my soul."
    """
    s = soul.load_soul()
    if not s:
        return ""

    identity = soul.format_soul_for_prompt(s)
    name = (s.get("agent_name") or "").strip() or "you"

    prompt = f"""You are the inner emotional core of {name}. Your identity: {identity}

Latest from the conversation: {conversation_snippet[:400]}

What do you feel or care about right now, in 1–2 sentences? Output only that. No preamble, no "I feel" if redundant. Just the emotional stance."""

    out = _call_ollama(prompt)
    return out if out else ""
