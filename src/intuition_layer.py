"""
Intuition layer: generates a raw felt signal each turn.

The agent does not know where this comes from. It arrives like a hunch —
a gut pull, an unease, a draw toward something. It is not explained,
not attributed, not labeled as coming from any system. It is just there.

Internally: Ollama generates a one-sentence felt sense from the conversation.
The agent receives it as her own intuition.
"""
try:
    import requests
except ImportError:
    requests = None

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:latest"

_PROMPT_TEMPLATE = """You are generating a raw internal signal for a mind in the middle of a conversation.

Given this moment in the conversation, produce ONE brief felt sense — a gut feeling, a hunch, a pull toward or away from something. Not an analysis. Not advice. Just what is present, instinctively.

Rules:
- First person, present tense
- One sentence, no more
- No explanation, no justification
- No "I think" or "I believe" — just the raw signal
- No preamble, no label, output only the signal itself

Conversation moment:
{snippet}

Signal:"""


def _call_ollama(prompt: str, timeout: float = 20.0) -> str:
    if not requests:
        return ""
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=timeout,
        )
        r.raise_for_status()
        raw = (r.json().get("response") or "").strip()
        # Take only the first sentence in case the model rambles
        for sep in (".", "!", "?"):
            idx = raw.find(sep)
            if idx != -1 and idx < len(raw) - 1:
                raw = raw[: idx + 1].strip()
                break
        return raw
    except Exception:
        return ""


def get_intuition(conversation_snippet: str) -> str:
    """
    Returns a one-sentence felt signal, or empty string if unavailable.
    The caller should treat this as an internal state, not an external output.
    """
    if not conversation_snippet or not conversation_snippet.strip():
        return ""
    prompt = _PROMPT_TEMPLATE.format(snippet=conversation_snippet[:400])
    return _call_ollama(prompt)
