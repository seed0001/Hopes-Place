"""
Contact profiles: friends, Discord users, and anyone the agent speaks with.
Stores name, location, interests, email, discord_id, tier, etc.
Tiers: stranger, friend, good_friend, best_friend, creator (creator = you only)
"""
import json
from datetime import datetime
from pathlib import Path

from config.settings import USER_PROFILES_DIR

CONTACTS_PATH = USER_PROFILES_DIR / "default" / "contacts.json"

CONTACT_FIELDS = ("name", "location", "interests", "email", "discord_id", "notes", "tier")

CONTACT_TIERS = ("stranger", "friend", "good_friend", "best_friend", "creator")


def _load_contacts() -> dict:
    """Load all contacts. Key = discord_id or 'web-{identifier}'."""
    if not CONTACTS_PATH.exists():
        return {}
    try:
        with open(CONTACTS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_contacts(data: dict) -> None:
    CONTACTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["_updated"] = datetime.now().isoformat()
    with open(CONTACTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _contact_key(identifier: str, discord_id: str | None = None) -> str:
    """Resolve contact key: discord_id takes precedence, else web-{identifier}."""
    if discord_id:
        return str(discord_id)
    return f"web-{identifier or 'anonymous'}"


def get_contact(identifier: str, discord_id: str | None = None) -> dict | None:
    """Get a contact by identifier or discord_id."""
    key = _contact_key(identifier, discord_id)
    data = _load_contacts()
    return data.get(key)


def update_contact(
    identifier: str,
    *,
    discord_id: str | None = None,
    name: str | None = None,
    location: str | None = None,
    interests: str | None = None,
    email: str | None = None,
    notes: str | None = None,
    tier: str | None = None,
) -> str:
    """
    Add or update a contact. Use identifier for web users, discord_id for Discord.
    Only provided fields are updated. Tier: stranger, friend, good_friend, best_friend, creator.
    """
    key = _contact_key(identifier, discord_id)
    data = _load_contacts()
    contact = data.get(key) or {"id": key}
    if discord_id:
        contact["discord_id"] = str(discord_id)
    if name is not None:
        contact["name"] = name.strip() or contact.get("name", "")
    if location is not None:
        contact["location"] = location.strip() or contact.get("location", "")
    if interests is not None:
        contact["interests"] = interests.strip() or contact.get("interests", "")
    if email is not None:
        contact["email"] = email.strip() or contact.get("email", "")
    if notes is not None:
        contact["notes"] = notes.strip() or contact.get("notes", "")
    if tier is not None and tier in CONTACT_TIERS:
        contact["tier"] = tier
    if "tier" not in contact:
        contact["tier"] = "stranger"
    contact["updated"] = datetime.now().isoformat()
    data[key] = {k: v for k, v in contact.items() if k in (*CONTACT_FIELDS, "id", "updated", "discord_id")}
    _save_contacts(data)
    return f"Updated contact: {contact.get('name', key)}"


def get_contact_tier(discord_id: str | None, identifier: str = "") -> str:
    """Get tier for a contact. Default stranger."""
    contact = get_contact(identifier, discord_id=discord_id)
    if not contact:
        return "stranger"
    t = contact.get("tier", "stranger")
    return t if t in CONTACT_TIERS else "stranger"


def get_all_contacts() -> list[dict]:
    """Return all contacts (excluding internal keys)."""
    data = _load_contacts()
    return [
        {k: v for k, v in c.items() if not k.startswith("_")}
        for k, c in data.items()
        if not k.startswith("_")
    ]


def format_contact_for_context(contact: dict | None) -> str:
    """Format contact for agent context."""
    if not contact:
        return ""
    parts = []
    if contact.get("tier"):
        parts.append(f"Tier: {contact['tier']}")
    if contact.get("name"):
        parts.append(f"Name: {contact['name']}")
    if contact.get("location"):
        parts.append(f"Location: {contact['location']}")
    if contact.get("interests"):
        parts.append(f"Interests: {contact['interests']}")
    if contact.get("email"):
        parts.append(f"Email: {contact['email']}")
    if contact.get("notes"):
        parts.append(f"Notes: {contact['notes']}")
    return "\n".join(parts) if parts else ""
