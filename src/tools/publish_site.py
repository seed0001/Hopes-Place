"""Publish docs/ to GitHub (GitHub Pages when repo uses branch + /docs)."""
import os
import subprocess
from pathlib import Path

from config.settings import PROJECT_ROOT


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(PROJECT_ROOT), *args],
        capture_output=True,
        text=True,
        timeout=180,
    )


def publish_hope_site(commit_message: str = "") -> str:
    """
    Stage docs/, commit if needed, push to configured remote.
    Env: GITHUB_PAGES_REMOTE (default hopes-place), GITHUB_PAGES_BRANCH (default main).
    """
    docs = PROJECT_ROOT / "docs"
    if not docs.is_dir():
        return "Error: docs/ folder missing at project root. Create docs/ and add your site files."

    msg = (commit_message or "").strip() or "docs: update Hope's site"

    add = _git("add", "docs")
    if add.returncode != 0:
        return f"git add failed: {(add.stderr or add.stdout).strip()}"

    diff = _git("diff", "--cached", "--quiet")
    if diff.returncode == 0:
        return "Nothing new to publish — docs/ has no changes to commit."

    ci = _git("commit", "-m", msg)
    if ci.returncode != 0:
        return f"git commit failed: {(ci.stderr or ci.stdout).strip()}"

    remote = (os.environ.get("GITHUB_PAGES_REMOTE") or "hopes-place").strip() or "hopes-place"
    branch = (os.environ.get("GITHUB_PAGES_BRANCH") or "main").strip() or "main"

    if _git("remote", "get-url", remote).returncode != 0:
        remote = "origin"
        if _git("remote", "get-url", remote).returncode != 0:
            return (
                "No usable git remote (tried GITHUB_PAGES_REMOTE / hopes-place / origin). "
                "Add a remote pointing at GitHub or set GITHUB_PAGES_REMOTE."
            )

    pu = _git("push", remote, branch)
    if pu.returncode != 0:
        err = (pu.stderr or pu.stdout or "").strip()
        return (
            f"git push to {remote} {branch} failed: {err}\n"
            "Creator may need to run: gh auth login, or fix credentials / remote URL."
        )

    return (
        f"Published docs/ to {remote} ({branch}). "
        "GitHub Pages usually updates within 1–2 minutes."
    )
