"""Configuration for the assistive operating agent."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MEMORY_DIR = DATA_DIR / "memory"
USER_PROFILES_DIR = DATA_DIR / "profiles"
LOGS_DIR = PROJECT_ROOT / "logs"

KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"

for d in (DATA_DIR, MEMORY_DIR, USER_PROFILES_DIR, LOGS_DIR, KNOWLEDGE_DIR):
    d.mkdir(parents=True, exist_ok=True)

# xAI Grok
XAI_API_KEY = os.getenv("XAI_API_KEY", "")
XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = os.getenv("XAI_MODEL", "grok-3")

# Voice
EDGE_TTS_VOICE = "en-GB-RyanNeural"  # British male - Ryan

# Web (0.0.0.0 = accessible from phone on local network)
WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", "8765"))

# Cursor CLI (escalation when Doctor Mode exhausts attempts)
CURSOR_CLI_CMD = os.getenv("CURSOR_CLI_CMD", "agent")
CURSOR_API_KEY = os.getenv("CURSOR_API_KEY", "")

# Discord (bot + proactive outreach)
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_OWNER_ID = os.getenv("DISCORD_OWNER_ID", "")  # Travis's Discord user ID for DMs
