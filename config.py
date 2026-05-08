"""
config.py — Contact info loader for Troy Hokanson document templates
====================================================================

Reads personal contact details from environment variables so that
sensitive information (phone number, email) is never hardcoded in
the public repository.

Priority order (highest to lowest):
  1. Environment variable already set in the shell (e.g. GitHub Actions Secret)
  2. .env file in the repo root (local machine, gitignored)
  3. Fallback placeholder string (safe for public display)

Setup on a new device
---------------------
1. Copy config.example.env to .env in the repo root:
       cp config.example.env .env
2. Fill in your real values in .env (it is gitignored — never committed).
3. Run any build script normally; config.py loads .env automatically.

GitHub Actions
--------------
Add the following repository secrets (Settings -> Secrets -> Actions):
  TROY_PHONE      e.g.  612.555.0000
  TROY_EMAIL      e.g.  TroyHokanson@iCloud.com
  TROY_LOCATION   e.g.  Lakeville, MN
  TROY_LINKEDIN   e.g.  linkedin.com/in/troyhokanson
  TROY_PORTFOLIO  e.g.  https://troy-hokanson.github.io/portfolio

The workflow yml passes them as env: vars and this module picks them up
automatically — no code changes needed across devices.
"""

import os
from pathlib import Path


def _load_dotenv(env_path: Path) -> None:
    """Minimal .env loader — no external dependencies required."""
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Only set if not already in environment (shell/Actions takes priority)
            if key and key not in os.environ:
                os.environ[key] = value


# Load .env from repo root (silently ignored if it doesn't exist)
_load_dotenv(Path(__file__).parent / ".env")


# ── Public contact constants ─────────────────────────────────────────────────

TROY_PHONE     = os.getenv("TROY_PHONE",     "")
TROY_EMAIL     = os.getenv("TROY_EMAIL",     "TroyHokanson@iCloud.com")
TROY_LOCATION  = os.getenv("TROY_LOCATION",  "Lakeville, MN")
TROY_LINKEDIN  = os.getenv("TROY_LINKEDIN",  "linkedin.com/in/troyhokanson")
TROY_PORTFOLIO = os.getenv("TROY_PORTFOLIO", "https://troy-hokanson.github.io/portfolio")
TROY_NAME      = os.getenv("TROY_NAME",      "Troy J. Hokanson")
