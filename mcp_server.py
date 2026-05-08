"""
Read-only MCP server for the Troy Hokanson document-standards repository.

Exposes four tools to any MCP-compatible AI client (Claude Desktop, ChatGPT
with developer-mode connectors, Cursor, VS Code, etc.):

  list_files      — list every text file available in this repo
  read_file       — return the full contents of a repo file by name
  search_files    — grep a regex pattern across all text files
  fetch_standard  — shortcut to read one of the four locked-standard docs

Transport: stdio (run locally via `python mcp_server.py`).

Usage with Claude Desktop — add to claude_desktop_config.json:
  See claude_desktop_config.json in this repo for the ready-to-paste snippet.
"""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Server bootstrap
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.resolve()

# Files/patterns that are always excluded (binary, git internals, secrets)
_EXCLUDE_PATTERNS = (
    ".git/*",
    "*.docx",
    "*.pdf",
    "*.pyc",
    "__pycache__/*",
    ".env",
    "*.env",
)

# The four locked-standard documents available via fetch_standard
STANDARD_DOCS = {
    "HEADER_STANDARD.md": "Visual formatting standard (navy/gold header layout)",
    "VOICE_STANDARD.md": "Narrative voice standard (anti-AI markers, tone, punctuation)",
    "SYSTEM_PROMPT.md": "Universal system prompt — paste into any AI platform",
    "PLATFORM_SETUP.md": "Per-platform AI setup guide (ChatGPT, Claude, Perplexity, Manus)",
}

mcp = FastMCP(
    "Troy Hokanson Document Standards",
    instructions=(
        "Read-only access to the Troy Hokanson resume/CV document-standards repository. "
        "Use fetch_standard to load the locked formatting and voice rules before generating "
        "any resume, cover letter, or CV. Never modify files — this server is read-only."
    ),
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_excluded(rel: str) -> bool:
    """Return True if the relative path matches any exclusion pattern."""
    for pat in _EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(Path(rel).name, pat):
            return True
    return False


def _repo_text_files() -> list[Path]:
    """Return all readable text files in the repo, sorted, with exclusions applied."""
    files: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        if _is_excluded(rel):
            continue
        # Skip files under .github/agents (off-limits per policy)
        if rel.startswith(".github/agents"):
            continue
        files.append(path)
    return files


def _safe_resolve(filename: str) -> Path:
    """
    Resolve *filename* relative to REPO_ROOT and verify it stays inside the repo.
    Raises ValueError on path traversal attempts.
    """
    target = (REPO_ROOT / filename).resolve()
    if REPO_ROOT not in target.parents and target != REPO_ROOT:
        raise ValueError(f"Access denied: '{filename}' resolves outside the repository.")
    return target


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_files() -> str:
    """
    List every text file available in the Troy Hokanson document-standards repo.

    Returns a newline-separated list of relative file paths. Binary files
    (.docx, .pdf, .pyc) and git internals are excluded.
    """
    files = _repo_text_files()
    lines = [p.relative_to(REPO_ROOT).as_posix() for p in files]
    return "\n".join(lines) if lines else "(no files found)"


@mcp.tool()
def read_file(filename: str) -> str:
    """
    Return the full text contents of a repo file.

    Parameters
    ----------
    filename:
        Relative path from the repo root, e.g. "VOICE_STANDARD.md" or
        "tests/test_anti_ai_scan.py". Must not escape the repo root.
    """
    try:
        target = _safe_resolve(filename)
    except ValueError as exc:
        return f"ERROR: {exc}"

    rel = target.relative_to(REPO_ROOT).as_posix()
    if _is_excluded(rel) or rel.startswith(".github/agents"):
        return f"ERROR: '{filename}' is not accessible via this server."

    if not target.exists():
        return f"ERROR: '{filename}' does not exist in the repository."
    if not target.is_file():
        return f"ERROR: '{filename}' is a directory, not a file."

    try:
        return target.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"ERROR: '{filename}' is a binary file and cannot be read as text."


@mcp.tool()
def search_files(pattern: str, glob: str = "*.md *.py *.json *.txt") -> str:
    """
    Search all repo text files for lines matching a regex pattern.

    Parameters
    ----------
    pattern:
        A Python regex pattern (case-insensitive). Keep it simple —
        plain text searches work fine, e.g. "navy" or "forbidden phrase".
    glob:
        Space-separated glob patterns that restrict which files are searched.
        Defaults to Markdown, Python, JSON, and plain-text files.

    Returns a list of matching lines formatted as:
        <filename>:<line_number>: <line_content>
    Limited to 200 matches to keep responses manageable.
    """
    globs = glob.split()
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error as exc:
        return f"ERROR: Invalid regex pattern — {exc}"

    results: list[str] = []
    for path in _repo_text_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        if not any(fnmatch.fnmatch(path.name, g) for g in globs):
            continue
        try:
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if regex.search(line):
                    results.append(f"{rel}:{lineno}: {line}")
                    if len(results) >= 200:
                        results.append("... (result limit reached — refine your pattern)")
                        return "\n".join(results)
        except UnicodeDecodeError:
            continue

    return "\n".join(results) if results else f"(no matches for pattern: {pattern!r})"


@mcp.tool()
def fetch_standard(document: str) -> str:
    """
    Fetch one of the four locked-standard documents for Troy Hokanson's career docs.

    This is the **preferred first call** before writing any resume or cover letter.
    Load both HEADER_STANDARD.md and VOICE_STANDARD.md before generating output.

    Parameters
    ----------
    document:
        One of:
          "HEADER_STANDARD.md"  — visual formatting (navy/gold header layout)
          "VOICE_STANDARD.md"   — narrative voice rules and anti-AI phrase list
          "SYSTEM_PROMPT.md"    — universal system prompt for any AI platform
          "PLATFORM_SETUP.md"   — how to configure each AI platform
    """
    if document not in STANDARD_DOCS:
        valid = ", ".join(STANDARD_DOCS.keys())
        return (
            f"ERROR: '{document}' is not a recognized standard document. "
            f"Valid options: {valid}"
        )
    return read_file(document)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
