# MCP Server Setup Guide

This repository ships a read-only **Model Context Protocol (MCP) server** (`mcp_server.py`) that gives Claude, ChatGPT, and other MCP-compatible AI clients direct, live access to Troy's locked document standards — no manual copy-paste or file uploads required.

---

## What the server exposes

| Tool | What it does |
|---|---|
| `fetch_standard` | **Start here.** Returns the full text of one of the four locked-standard docs by name. |
| `read_file` | Returns the full text of any repo file by relative path. |
| `list_files` | Lists every accessible text file in the repo. |
| `search_files` | Regex-searches across all text files; returns matching lines with file and line number. |

### The four locked-standard documents (use `fetch_standard`)

| Document | Purpose |
|---|---|
| `HEADER_STANDARD.md` | Navy/gold header layout specification |
| `VOICE_STANDARD.md` | Narrative voice rules, anti-AI phrase list, punctuation rules |
| `SYSTEM_PROMPT.md` | Universal system prompt — the AI's core directive |
| `PLATFORM_SETUP.md` | Per-platform AI configuration guide |

### What the server does NOT expose

- `.env` files and any file matching `*.env` (credentials)
- `.git/` internals
- `.github/agents/` directory (agent instructions)
- Binary files: `.docx`, `.pdf`, `.pyc`
- Anything outside the repository root (path traversal is blocked)

---

## Prerequisites

```bash
# From the repo root — install MCP server dependency alongside existing deps
pip install -r requirements.txt
```

---

## 1. Claude Desktop (preferred — local MCP)

Claude Desktop connects to the server over stdio. Edit your Claude Desktop config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Paste the following block (replacing the path with the actual location of your clone):

```json
{
  "mcpServers": {
    "troy-hokanson-standards": {
      "command": "python",
      "args": ["/path/to/troy-hokanson-resume-cover-cv/mcp_server.py"],
      "env": {}
    }
  }
}
```

A ready-to-paste snippet is also saved as `claude_desktop_config.json` in this repo — edit the path, then copy it into your Claude Desktop config.

Restart Claude Desktop. The four MCP tools will appear automatically in every conversation.

**Trigger phrase:** Once connected, just say:
> *"Fetch HEADER_STANDARD.md and VOICE_STANDARD.md from the MCP server, then write a cover letter for [Role]."*

Claude will call `fetch_standard` twice and apply the live standards before writing a word.

---

## 2. ChatGPT (Custom GPT + Actions)

ChatGPT supports only **remote** MCP connectors. Because this repo's files are publicly available on GitHub's raw CDN, the existing Custom GPT action (`chatgpt_action_schema.json`) provides equivalent live-fetch capability without running a local server.

See **Section 1** of `PLATFORM_SETUP.md` for full Custom GPT setup steps. The action schema now covers all four standard documents (`HEADER_STANDARD.md`, `VOICE_STANDARD.md`, `SYSTEM_PROMPT.md`, `PLATFORM_SETUP.md`).

If you have a publicly hosted server that runs `mcp_server.py` over HTTP/SSE, you can also add it as a custom connector:

1. In ChatGPT, go to **Settings → Connectors → Add custom connector**
2. Enable **Developer Mode** in Settings → Advanced
3. Enter your server URL and any required auth token
4. ChatGPT will discover the four tools automatically

---

## 3. Perplexity

Perplexity Spaces do not yet support inbound MCP connectors as a client. The recommended integration remains the system-prompt + file-upload approach described in `PLATFORM_SETUP.md` Section 4.

If you need Perplexity to call the MCP server, use the Perplexity **API** with the `mcp` Python client, or route requests through an MCP-compatible orchestration layer (LangChain, LlamaIndex, etc.) that calls the server on Perplexity's behalf.

---

## 4. Other MCP-compatible clients

Any client that supports the MCP stdio transport works with `mcp_server.py`:

| Client | Config location |
|---|---|
| **Cursor** | `.cursor/mcp.json` in your project, same JSON format as Claude Desktop |
| **VS Code (GitHub Copilot)** | `.vscode/mcp.json`, same JSON format |
| **Windsurf** | `~/.codeium/windsurf/mcp_settings.json`, same JSON format |

Use the same JSON snippet from Section 1, updating the path for each client's config file.

---

## Testing the server locally

```bash
# Smoke-test: list available files
python - <<'EOF'
import subprocess, json
result = subprocess.run(
    ["python", "mcp_server.py"],
    input=json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}
    }) + "\n",
    capture_output=True, text=True, timeout=10
)
print(result.stdout[:500])
EOF
```

Or simply run the existing unit tests (they do not depend on the MCP server):

```bash
python -m pytest tests/ -v
```
