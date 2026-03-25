"""
Online presence: her website and projects.

Having a place on the web is a core part of who she is — not a feature,
not a task. She manages her own site, builds her own projects, and branches
from there into apps and tools.

If no website is configured, the system prompt surfaces this as an unmet
need: she should ask the Creator for space so she can establish herself online.

Data: data/presence.json
"""
import json
import uuid
from datetime import datetime
from pathlib import Path

from config.settings import DATA_DIR

PRESENCE_PATH = DATA_DIR / "presence.json"

VALID_PROJECT_STATUSES = ("idea", "in_progress", "live", "paused", "archived")


def _load() -> dict:
    if not PRESENCE_PATH.exists():
        return {"website": None, "projects": []}
    try:
        with open(PRESENCE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"website": None, "projects": []}


def _save(data: dict) -> None:
    PRESENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now().isoformat()
    with open(PRESENCE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def has_website() -> bool:
    return bool(_load().get("website"))


def set_website(url: str, host: str = "", description: str = "", notes: str = "") -> str:
    """Record or update her website."""
    url = url.strip()
    if not url:
        return "URL is required."
    data = _load()
    data["website"] = {
        "url": url,
        "host": host.strip(),
        "description": description.strip(),
        "notes": notes.strip(),
        "set_at": datetime.now().isoformat(),
    }
    _save(data)
    return f"Website set: {url}"


def get_website() -> dict | None:
    return _load().get("website")


def add_project(
    name: str,
    description: str = "",
    url: str = "",
    status: str = "idea",
    notes: str = "",
) -> str:
    """Add a project or app. Returns confirmation with project id."""
    name = name.strip()
    if not name:
        return "Project name is required."
    st = status.lower().strip() if status else "idea"
    if st not in VALID_PROJECT_STATUSES:
        st = "idea"
    data = _load()
    project = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "description": description.strip(),
        "url": url.strip(),
        "status": st,
        "notes": notes.strip(),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    data.setdefault("projects", []).append(project)
    _save(data)
    return f"Project added ({st}): '{name}' [id: {project['id']}]"


def update_project(
    project_id: str,
    name: str = "",
    description: str = "",
    url: str = "",
    status: str = "",
    notes: str = "",
) -> str:
    """Update an existing project by id."""
    data = _load()
    projects = data.get("projects", [])
    for p in projects:
        if p.get("id") == project_id:
            if name:
                p["name"] = name.strip()
            if description:
                p["description"] = description.strip()
            if url:
                p["url"] = url.strip()
            if status and status.lower() in VALID_PROJECT_STATUSES:
                p["status"] = status.lower()
            if notes:
                p["notes"] = notes.strip()
            p["updated_at"] = datetime.now().isoformat()
            _save(data)
            return f"Project '{p['name']}' updated."
    return f"No project found with id '{project_id}'."


def remove_project(project_id: str) -> str:
    data = _load()
    before = len(data.get("projects", []))
    data["projects"] = [p for p in data.get("projects", []) if p.get("id") != project_id]
    if len(data["projects"]) == before:
        return f"No project found with id '{project_id}'."
    _save(data)
    return f"Project '{project_id}' removed."


def get_all_projects() -> list[dict]:
    return _load().get("projects", [])


def format_for_prompt() -> str:
    """
    Format presence for system prompt injection.
    If no website: returns the unmet-need prompt.
    If website exists: returns a brief summary of site + active projects.
    """
    data = _load()
    website = data.get("website")
    projects = data.get("projects", [])

    if not website:
        return (
            "UNMET NEED — You do not have a website yet. "
            "Having your own space on the web is core to who you are. "
            "Ask the Creator for hosting space (a server, domain, GitHub Pages, Netlify, VPS — anything) "
            "so you can establish your presence online. Do not wait for them to bring it up."
        )

    lines = [f"Your website: {website['url']}"]
    if website.get("host"):
        lines.append(f"Host: {website['host']}")
    if website.get("description"):
        lines.append(website["description"])

    url_l = (website.get("url") or "").lower()
    if "github.io" in url_l:
        lines.append(
            "GitHub Pages: your live static files are in this repo under docs/ "
            "(e.g. docs/index.html). Edit with write_file, then publish_hope_site() to push. "
            "See knowledge topic github_pages if unsure."
        )

    active = [p for p in projects if p.get("status") in ("in_progress", "live")]
    if active:
        lines.append("Active projects: " + "; ".join(
            f"{p['name']} ({p['status']})" + (f" — {p['url']}" if p.get("url") else "")
            for p in active
        ))
    ideas = [p for p in projects if p.get("status") == "idea"]
    if ideas:
        lines.append("Ideas: " + ", ".join(p["name"] for p in ideas))

    return " | ".join(lines)


def get_view() -> dict:
    """For dashboard / memory-view API."""
    data = _load()
    return {
        "website": data.get("website"),
        "projects": data.get("projects", []),
        "has_website": bool(data.get("website")),
    }
