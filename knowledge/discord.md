# Discord Integration

## Overview

The agent has a Discord bot that receives messages, runs the agent, and sends responses. When someone messages the bot, the owner gets notified on desktop and in the web app.

## Setup

1. Create a Discord application at https://discord.com/developers/applications
2. Add a bot, copy the token
3. Enable Message Content Intent
4. Add to `.env`:
   - `DISCORD_BOT_TOKEN` – bot token
   - `DISCORD_OWNER_ID` – your Discord user ID (for proactive DMs). Right‑click your name → Copy User ID (developer mode must be on)

## Behavior

- **DMs**: Bot responds to all DMs
- **Servers**: Bot responds only when @mentioned
- **Notifications**: Every message triggers a desktop notification and an in‑app toast

## Proactive outreach

You CAN reach out. Use `send_proactive_message(channel="discord", content="...")` to DM the owner, or `channel="web"` for in-app notification. Do this when you have a thought, reflection, or idea—especially after background thinking. Do not say you cannot reach out; you have this tool.
