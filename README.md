# Assistive Operating Agent

An assistive AI agent powered by Grok 3 (xAI), with full system access, multi-layer memory, Doctor Mode (self-healing), voice interface (Edge TTS - Ryan), and web dashboard.

## Setup

1. **Create `.env`** from the example:
   ```
   cp .env.example .env
   ```
   Add your xAI API key:
   ```
   XAI_API_KEY=your_key_here
   XAI_MODEL=grok-3
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run:**
   ```
   python main.py
   ```
   Dashboard: http://127.0.0.1:8765

## Discord (optional)

Add to `.env`:
```
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_OWNER_ID=your_discord_user_id
```

When configured, the agent receives DMs and @mentions, responds, and notifies you on desktop and in the web app. He can proactively message you via Discord or the web app, and builds contact profiles (name, location, interests, email) on everyone he talks to. See `knowledge/discord.md` and `knowledge/contacts.md`.

## Features

- **Voice**: Record (no auto-stop) → Stop → Send. Edge TTS (Ryan, British male) for responses.
- **Web dashboard**: Chat, voice controls, toggles. Markdown tables render properly.
- **Tools**: Files, processes (`list_processes`, `is_process_running`), commands, web search, build, sub-agents, DAG, knowledge base.
- **Sub-agents**: `process_monitor.py` (logs processes), `conversation_prompt.py` (periodic prompts). Spawn via `spawn_subagent`.
- **Ollama GUI**: Run `python ollama_model_selector.py` to load Ollama models (requires Ollama on localhost).
- **Memory**: 5-layer (immediate, short-term, working, episodic, user profile).
- **Doctor Mode**: Self-healing; escalates to Cursor CLI after 3 failed attempts.

## API Key

Create a `.env` file in the project root with your xAI API key. Get keys at [console.x.ai](https://console.x.ai).
