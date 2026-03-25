# GitHub Pages — Hope's public site

## Live URL

After GitHub Pages is enabled, the site is typically:

`https://<user>.github.io/<repo>/`

## Where files live in this project

Static files for the **public** site are under **`docs/`** at the project root (e.g. `docs/index.html`).

GitHub repo settings must use **Build and deployment → Deploy from a branch → `main` → `/docs`**.

## How Hope updates the site

1. Edit files with **`write_file`** using paths like `docs/index.html` or `docs/css/style.css`.
2. When ready to go live, call **`publish_hope_site(commit_message="short description of changes")`**.
   That stages `docs/`, commits, and pushes to the git remote (default `hopes-place`, or `GITHUB_PAGES_REMOTE` / `GITHUB_PAGES_BRANCH` env vars).

If `publish_hope_site` fails on push, the Creator may need to sign in to Git (`gh auth login` or credential manager) or fix the remote URL.

## Record the URL

Call **`set_website(url='...', host='GitHub Pages', ...)`** so presence and prompts stay aligned with the live link.
