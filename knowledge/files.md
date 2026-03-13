# File Operations

## read_file

**When to use:** User wants to see file contents, check config, read code, inspect logs.

**How:**
- `path`: Full or relative path. Supports `~` for home. Use forward slashes or backslashes.
- Returns file contents or an error if not found.

**Examples:**
- Read config: `read_file("config/settings.py")`
- Read env: `read_file(".env")` (be careful with secrets)
- Check log: `read_file("logs/agent.log")`

**Tips:** Use list_dir first if unsure of the path. On Windows, paths like `C:/Users/name/file.txt` work.

---

## write_file

**When to use:** User wants to create or overwrite a file, save content, write config.

**How:**
- `path`: Where to write. Parent dirs are created if missing.
- `content`: Full content to write (overwrites existing).

**Examples:**
- Create file: `write_file("notes.txt", "User notes here")`
- Update config: read first, modify, then write back.

**Tips:** For appending, read first, concatenate, then write. Be careful not to overwrite important files.

---

## list_dir

**When to use:** Explore folders, find files, see project structure, locate a file.

**How:**
- `path`: Optional. Defaults to current working directory if empty.
- Returns directory entries (folders show `/`).

**Examples:**
- List current: `list_dir("")` or `list_dir(".")`
- Explore project: `list_dir("src")`
