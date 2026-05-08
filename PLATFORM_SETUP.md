# Cross-Platform AI Setup Guide

This guide explains how to configure ChatGPT, Claude, Gemini, Perplexity, and Manus to automatically apply your formatting and voice standards whenever you ask them to write a resume or cover letter.

The goal is to make this GitHub repository the **single source of truth**. If you update a rule in `VOICE_STANDARD.md` here, every AI platform instantly uses the new rule without you having to update them individually.

---

## Preferred: MCP server (Claude Desktop, Cursor, VS Code, and more)

This repo ships `mcp_server.py` — a read-only Model Context Protocol (MCP) server that gives any MCP-compatible AI client **live, direct access** to the locked standard documents, without manual copy-paste or file uploads.

> **See [`MCP_SETUP.md`](./MCP_SETUP.md) for the full MCP setup guide.**

Quick start for Claude Desktop — add this to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

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

For platforms that do not support MCP client connections (Gemini, Perplexity Spaces), use the manual prompt + file-upload method described below.

---

## 1. ChatGPT (Custom GPT)

ChatGPT supports "Actions," which means it can literally fetch the live files from GitHub every time it runs. This is the most powerful integration.

### Setup Steps:
1. Go to ChatGPT -> **Explore GPTs** -> **Create** (top right)
2. Name it "Troy's Career Strategist"
3. In the **Instructions** box, paste the entire contents of [`SYSTEM_PROMPT.md`](./SYSTEM_PROMPT.md)
4. Scroll down and click **Create new action**
5. In the **Schema** box, paste the entire contents of [`chatgpt_action_schema.json`](./chatgpt_action_schema.json)
6. Click **Save** (top right)

**How it works:** When you say "Write a cover letter for a Fraud Analyst role," the GPT will automatically trigger the action, fetch the live standards from GitHub, and apply them. The action schema covers all four locked-standard documents: `HEADER_STANDARD.md`, `VOICE_STANDARD.md`, `SYSTEM_PROMPT.md`, and `PLATFORM_SETUP.md`.

**Alternatively (ChatGPT Developer Mode):** ChatGPT supports remote MCP connectors. If you host `mcp_server.py` on a public endpoint (HTTP/SSE), go to **Settings → Connectors → Add custom connector**, enable **Developer Mode**, and enter your server URL. See `MCP_SETUP.md` Section 2 for details.

---

## 2. Claude (claude.ai Projects / Claude Desktop)

**Preferred:** use the MCP server with Claude Desktop — it gives Claude live access to all standards without any manual uploads. See the MCP quick-start at the top of this file and `MCP_SETUP.md` for full instructions.

**Fallback (claude.ai Projects — no MCP):** Claude Projects cannot do live web fetching via Actions, but they have a massive context window and "Project Knowledge."

### Setup Steps:
1. Go to Claude -> **Projects** -> **Create Project**
2. Name it "Career Documents"
3. In the **Custom Instructions** box, paste the contents of [`SYSTEM_PROMPT.md`](./SYSTEM_PROMPT.md)
4. Under **Project Knowledge**, you must manually upload the `HEADER_STANDARD.md` and `VOICE_STANDARD.md` files from this repo.

**How it works (Projects fallback):** Claude will read the uploaded files as its ground truth. *Note: If you update the standards in GitHub, you must re-upload the files to Claude's Project Knowledge. With the MCP server, this step is automatic.*

---

## 3. Gemini (Google AI Studio / Gems)

Gemini Gems work similarly to Claude Projects — they rely on static knowledge.

### Setup Steps:
1. Go to Gemini -> **Gem manager** -> **New Gem**
2. Name it "Troy's Career Strategist"
3. In the **Instructions** box, paste the contents of [`SYSTEM_PROMPT.md`](./SYSTEM_PROMPT.md)
4. Under **Uploaded files**, attach `HEADER_STANDARD.md` and `VOICE_STANDARD.md`

**How it works:** The Gem will use the attached files to enforce the voice and format rules. Like Claude, you must re-upload them if the GitHub repo changes.

---

## 4. Perplexity (Spaces)

Perplexity Spaces do not yet support inbound MCP client connections, so the system-prompt + file-upload approach remains the best option here.

**For MCP-based Perplexity integration**, see `MCP_SETUP.md` Section 3 (API / orchestration layer approach).

### Setup Steps:
1. Go to Perplexity -> **Spaces** -> **Create Space**
2. Name it "Career Docs"
3. In the **Space Prompt** box, paste the contents of [`SYSTEM_PROMPT.md`](./SYSTEM_PROMPT.md)
4. Under **Files**, upload `HEADER_STANDARD.md` and `VOICE_STANDARD.md`

---

## 5. Manus

Manus has native GitHub integration and a full sandboxed environment, making it the most capable platform for actually *building* the DOCX and PDF files.

### Setup Steps:
You don't need to configure a custom prompt for Manus. Simply tell Manus:
> *"Clone `troyhokanson/troy-hokanson-resume-cover-cv`, read the standards, and build me a resume for [Role]."*

Manus will automatically clone the repo, read the live standards, and execute the Python build scripts (`docx_header.py` / `pdf_header.py`) to generate the actual files.
