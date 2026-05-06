"""
Unit tests for config.py — verifies env-var loading and safe fallbacks.

Run from the workspace root:
    python -m pytest templates/tests/ -v
"""

import os
import sys
import importlib
import pytest

_here = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.dirname(_here)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)


def _reload_config(env_overrides: dict) -> dict:
    """Reload config module with specific env vars, return captured attribute dict."""
    _KEYS = ["TROY_PHONE", "TROY_EMAIL", "TROY_LOCATION",
             "TROY_LINKEDIN", "TROY_PORTFOLIO", "TROY_NAME"]
    original = {k: os.environ.get(k) for k in _KEYS}

    # Remove all keys first, then apply overrides
    for k in _KEYS:
        os.environ.pop(k, None)
    for k, v in env_overrides.items():
        os.environ[k] = v

    import config
    importlib.reload(config)
    # Capture values before restoring environment
    captured = {k: getattr(config, k) for k in
                ["TROY_NAME", "TROY_PHONE", "TROY_EMAIL",
                 "TROY_LOCATION", "TROY_LINKEDIN", "TROY_PORTFOLIO"]}

    # Restore original environment and reload back to baseline
    for k in _KEYS:
        os.environ.pop(k, None)
    for k, v in original.items():
        if v is not None:
            os.environ[k] = v
    importlib.reload(config)

    return captured


class TestConfigFallbacks:
    def test_troy_name_has_fallback(self):
        cfg = _reload_config({})
        assert cfg["TROY_NAME"]

    def test_troy_location_has_fallback(self):
        cfg = _reload_config({})
        assert cfg["TROY_LOCATION"]

    def test_troy_linkedin_has_fallback(self):
        cfg = _reload_config({})
        assert cfg["TROY_LINKEDIN"]

    def test_troy_portfolio_has_fallback(self):
        cfg = _reload_config({})
        assert cfg["TROY_PORTFOLIO"]

    def test_troy_phone_empty_when_unset(self):
        cfg = _reload_config({})
        # Phone intentionally has no default so it is omitted from headers
        assert cfg["TROY_PHONE"] == ""


class TestConfigEnvVarOverride:
    def test_env_var_overrides_fallback(self):
        cfg = _reload_config({"TROY_NAME": "Jane Q. Tester"})
        assert cfg["TROY_NAME"] == "Jane Q. Tester"

    def test_phone_set_via_env(self):
        cfg = _reload_config({"TROY_PHONE": "612.555.1234"})
        assert cfg["TROY_PHONE"] == "612.555.1234"

    def test_email_set_via_env(self):
        cfg = _reload_config({"TROY_EMAIL": "test@example.com"})
        assert cfg["TROY_EMAIL"] == "test@example.com"


class TestConfigNoSensitiveHardcoding:
    def test_phone_not_hardcoded_in_source(self):
        """Phone must be empty string when env var is absent — no hardcoded number."""
        import config as cfg_mod
        src_path = os.path.join(_repo_root, "config.py")
        with open(src_path) as f:
            source = f.read()
        # Phone fallback must be an empty string, never a real number
        import re
        # Find TROY_PHONE getenv line
        match = re.search(r'TROY_PHONE\s*=\s*os\.getenv\([^)]+\)', source)
        assert match, "TROY_PHONE line not found"
        assert '""' in match.group() or "''" in match.group(), \
            f"TROY_PHONE fallback must be empty string, got: {match.group()}"
