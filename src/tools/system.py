"""System access tools: files, processes, clipboard, system info."""
import asyncio
import os
import platform
import shutil
import subprocess
from pathlib import Path


async def read_file(path: str) -> str:
    """Read file contents."""
    p = Path(path).expanduser()
    if not p.exists():
        return f"Error: File not found: {path}"
    if not p.is_file():
        return f"Error: Not a file: {path}"
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error reading file: {e}"


async def write_file(path: str, content: str) -> str:
    """Write content to file."""
    p = Path(path).expanduser()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Written to {path}"
    except Exception as e:
        return f"Error writing file: {e}"


async def list_dir(path: str) -> str:
    """List directory contents."""
    p = Path(path).expanduser() if path else Path.cwd()
    if not p.exists():
        return f"Error: Path not found: {path or '.'}"
    if not p.is_dir():
        return f"Error: Not a directory: {p}"
    try:
        items = list(p.iterdir())
        lines = [f"  {x.name}{'/' if x.is_dir() else ''}" for x in sorted(items, key=lambda x: (not x.is_dir(), x.name))]
        return "\n".join(lines) if lines else "(empty)"
    except Exception as e:
        return f"Error listing: {e}"


async def run_command(cmd: str, cwd: str | None = None, timeout: int = 60) -> str:
    """Run shell command. Use carefully."""
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            cwd=cwd or os.getcwd(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out_bytes, err_bytes = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        out = (out_bytes or b"").decode("utf-8", errors="replace").strip()
        err = (err_bytes or b"").decode("utf-8", errors="replace").strip()
        if err:
            return f"stdout:\n{out}\n\nstderr:\n{err}\n\nexit: {proc.returncode}"
        return f"{out}\n\nexit: {proc.returncode}"
    except asyncio.TimeoutError:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error: {e}"


async def list_processes(max_lines: int = 50) -> str:
    """List running processes. Works on Windows and Unix."""
    try:
        if platform.system() == "Windows":
            proc = await asyncio.create_subprocess_shell(
                'powershell -NoProfile -Command "Get-Process | Select-Object Name, Id, CPU, WorkingSet | Sort-Object CPU -Descending | Format-Table -AutoSize"',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            proc = await asyncio.create_subprocess_shell(
                "ps aux",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        out, err = await proc.communicate()
        text = (out or b"").decode("utf-8", errors="replace").strip()
        if err:
            err_text = (err or b"").decode("utf-8", errors="replace").strip()
            if err_text and "Error" in err_text:
                # Fallback: tasklist on Windows
                if platform.system() == "Windows":
                    proc2 = await asyncio.create_subprocess_shell(
                        "tasklist /FO TABLE",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    out2, _ = await proc2.communicate()
                    text = (out2 or b"").decode("utf-8", errors="replace").strip()
                else:
                    return f"Error: {err_text}"
        lines = text.splitlines()
        if max_lines and len(lines) > max_lines:
            lines = lines[:max_lines]
            text = "\n".join(lines) + f"\n... ({max_lines} of many shown)"
        return text
    except Exception as e:
        return f"Error listing processes: {e}"


async def is_process_running(name: str) -> str:
    """Check if a process is running by name (case-insensitive, partial match). Returns PID(s) or 'not found'."""
    try:
        if platform.system() == "Windows":
            cmd = f'powershell -NoProfile -Command "Get-Process | Where-Object {{ $_.ProcessName -like \'*{name}*\' }} | Select-Object Name, Id | Format-Table -AutoSize"'
        else:
            cmd = f"pgrep -fl {name}" if name else "echo 'provide name'"
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        out, err = await proc.communicate()
        text = (out or b"").decode("utf-8", errors="replace").strip()
        if not text or "Error" in (err or b"").decode("utf-8", errors="replace"):
            return f"Process matching '{name}': not found"
        return f"Process matching '{name}':\n{text}"
    except Exception as e:
        return f"Error: {e}"


async def get_system_info() -> str:
    """Get basic system info."""
    return (
        f"OS: {platform.system()} {platform.release()}\n"
        f"Machine: {platform.machine()}\n"
        f"User: {os.environ.get('USERNAME', os.environ.get('USER', 'unknown'))}\n"
        f"CWD: {os.getcwd()}"
    )
