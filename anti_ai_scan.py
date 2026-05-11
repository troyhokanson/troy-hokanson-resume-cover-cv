"""
Anti-AI / Voice scan — MANDATORY automatic gate for every Hokanson document.

Codifies the rules from linkedin-profile-optimizer SKILL.md Sections B/C/D and
the Pre-Submission Document Checklist. Run BEFORE share_file on any resume,
cover letter, CV, recruiter packet, bio, or one-pager.

Voice baseline: 54-year-old Gen-X medically retired Minnesota detective,
M.A. (GPA 3.94), 19 years adjunct teaching, empathetic + investigator-precise.

Usage:
    from templates.anti_ai_scan import scan_pdf, FailedScan

    # Standard build (PTSD-scope hard block active):
    scan_pdf("/path/to/Hokanson_Resume_Foo.pdf", doc_type="resume")

    # ICAC / child-safety role build (gate opens for CSAM / exploitation terms):
    scan_pdf("/path/to/Hokanson_Resume_Roblox.pdf", doc_type="resume", allow_icac=True)

doc_type  = "resume" | "cover" | "cv" | "bio"
allow_icac = False (default) | True
             When True, CSAM / child-exploitation / ICAC training references
             are permitted. All other PTSD-scope terms (homicide, lethal force,
             sexual assault, criminal sexual conduct, human trafficking) remain
             blocked regardless of this flag.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

try:
    from config import TROY_NAME, TROY_PHONE, TROY_EMAIL
except ImportError:
    TROY_NAME = "Troy J. Hokanson"
    TROY_PHONE = ""
    TROY_EMAIL = ""

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


class FailedScan(Exception):
    """Raised when a document fails the anti-AI / voice scan."""


# ---- Forbidden phrases (Section B of skill) ----
FORBIDDEN_PHRASES = [
    "I bring", "I offer", "leveraged", "harnessed", "spearheaded", "championed",
    "passionate about", "dynamic", "synergy", "synergies", "robust",
    "comprehensive", "cutting-edge", "best-in-class", "results-driven",
    "detail-oriented", "proven track record", "in today's environment",
    "in conclusion", "to summarize", "it is worth noting", "I am excited to",
    "I would be remiss", "at the end of the day", "needless to say",
    "with that said", "that being said", "moving forward", "going forward",
    "touch base", "circle back", "value-add", "value add", "impactful",
    "game-changer", "paradigm shift", "holistic approach", "deep dive",
    "bandwidth", "optimized", "streamlined", "facilitated", "delivered value",
    "implemented solutions", "drove outcomes", "empowered", "transformed",
    "transforming", "I look forward to discussing",
]

# Phrases the user has explicitly flagged as AI-sounding in this lineage
EXTRA_FLAGGED = [
    "ramping on",          # AI-business cliche substitute for "learning"
    "fundamentally",       # AI throat-clearing adverb in cover letters
    "in order to",         # filler - use "to"
    "utilize", "utilized", "utilizing",  # use "use"
    "utilization",
    "myriad of",
    "plethora",
    "delve into", "delving",
    "tapestry",
    "navigate the complexities",
    "ever-evolving", "ever-changing",
    "seamlessly",
    "elevate",
    "unlock",
    "world-class",
    "best practices",      # only flagged in flowing prose, not section headings

    # Redundant skill terminology (X and Y where Y is already inside X)
    "OSINT and open-source",         # use OSINT only
    "interviews and interrogations",  # use investigative interviewing
    "surveillance and monitoring",    # use surveillance
    "training and mentoring",         # use field training or mentorship per context
    "remote and online",              # use remote instruction
    "research and analysis",          # use investigative analysis
    "leadership and management",      # use leadership
    "planning and coordination",      # use operational coordination
]

ALL_FORBIDDEN = FORBIDDEN_PHRASES + EXTRA_FLAGGED

# ---- PTSD-scope term sets ----
# Always-blocked: never appropriate in any Hokanson document regardless of role.
PTSD_TERMS_ALWAYS_BLOCKED = [
    "homicide",
    "death investigation",
    "lethal force",
    "sexual assault",
    "criminal sexual conduct",
    "human trafficking",
]

# ICAC-gated: blocked by default. Pass allow_icac=True for documents targeting
# child-safety / ICAC platform roles (e.g. Roblox Trust & Safety, NCMEC,
# tech platform child-safety teams) where this experience and ICAC training
# is directly relevant and expected by the hiring team.
PTSD_TERMS_ICAC_GATED = [
    "CSAM",
    "child sexual",
    "child abuse",
    "child exploitation",
    "ICAC",
]


def _extract(pdf_path: str) -> str:
    if pdfplumber is None:
        raise RuntimeError("pdfplumber not installed - cannot scan PDF")
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages)


def _strip_header(text: str) -> str:
    """Remove the locked navy header repeated rows (name + contact line)
    so they are not falsely flagged."""
    _email_user = TROY_EMAIL.split("@")[0] if "@" in TROY_EMAIL else TROY_EMAIL
    out = []
    for line in text.splitlines():
        s = line.strip()
        if TROY_NAME and s.startswith(TROY_NAME):
            continue
        if s.startswith("---") or set(s) <= {"-", " "}:
            continue
        if TROY_PHONE and TROY_PHONE in s and _email_user and _email_user in s:
            continue
        out.append(line)
    return "\n".join(out)


def scan_text(
    text: str,
    doc_type: str = "resume",
    allow_icac: bool = False,
) -> list[str]:
    """Return list of violation strings. Empty list = pass.

    Parameters
    ----------
    text       : raw document text
    doc_type   : "resume" | "cover" | "cv" | "bio"
    allow_icac : When True, CSAM / child-exploitation / ICAC training terms
                 are permitted. Use only for documents targeting ICAC or
                 child-safety roles. All other PTSD-scope terms remain blocked.
    """
    doc_type = doc_type.lower()
    body = _strip_header(text)
    failures = []

    # 1. Em / en dashes - never in any document
    if "\u2014" in body:
        failures.append(f"Em dash found ({body.count(chr(0x2014))}x). Replace with period or rewrite.")
    if "\u2013" in body:
        failures.append(f"En dash found ({body.count(chr(0x2013))}x). Use 'to' in prose, plain hyphen in date fields.")

    # 2. Exclamation points - never
    if "!" in body:
        failures.append(f"Exclamation point(s) found ({body.count('!')}x). Forbidden in professional content.")

    # 3. Ellipses for stylistic effect
    if "..." in body or "\u2026" in body:
        failures.append("Ellipsis found. Forbidden - use a period or rewrite.")

    # 4. Curly / smart quotes (Word auto-substitution leakage)
    curly = sum(body.count(c) for c in "\u201c\u201d\u2018\u2019")
    if curly:
        failures.append(f"Curly/smart quotes found ({curly}x). Use straight quotes only.")

    # 5. Semicolons - forbidden in cover letters and About/bio sections
    if doc_type in ("cover", "bio") and ";" in body:
        failures.append(f"Semicolon(s) found in {doc_type} ({body.count(';')}x). Forbidden - split into separate sentences.")

    # 6. Forbidden phrases (whole-word, case-insensitive)
    for p in ALL_FORBIDDEN:
        pattern = re.escape(p).replace(r"\'", r"['']")
        if re.search(rf"(?<![A-Za-z]){pattern}(?![A-Za-z])", body, re.IGNORECASE):
            failures.append(f"Forbidden phrase: '{p}'")

    # 7. "As a [Title]..." paragraph opener
    if re.search(r"(?m)^\s*As an? [A-Z][a-z]+", body):
        failures.append("Paragraph opens with 'As a [Title]...' - strongest AI opener pattern.")

    # 8. Cover-letter-specific structural rules
    if doc_type == "cover":
        if re.search(r"I look forward", body, re.IGNORECASE):
            failures.append("Cover letter contains 'I look forward...' - most-overused AI closing.")
        for bad_close in ["Sincerely,", "Best regards,", "Best,", "Thank you,", "Kind regards,", "Warm regards,"]:
            if bad_close in body:
                failures.append(f"Cover letter uses '{bad_close}' - must be 'Respectfully,'")
        contractions = re.findall(
            r"\b(?:I'm|I've|I'll|I'd|don't|won't|can't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't"
            r"|wouldn't|shouldn't|couldn't|it's|that's|there's|here's|what's|who's|let's"
            r"|you're|we're|they're|you'll|we'll|they'll|you've|we've|they've|you'd|we'd|they'd)\b",
            body, re.IGNORECASE,
        )
        if len(contractions) > 2:
            failures.append(f"Cover letter has {len(contractions)} contractions (max 2): {contractions}")

    # 9. Resume / CV bullet contractions - zero allowed (possessives like Master's exempted)
    if doc_type in ("resume", "cv"):
        bullet_contractions = re.findall(
            r"\b(?:I'm|I've|I'll|I'd|don't|won't|can't|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't"
            r"|wouldn't|shouldn't|couldn't|it's|that's|there's|here's|let's|you're|we're|they're)\b",
            body, re.IGNORECASE,
        )
        if bullet_contractions:
            failures.append(f"{doc_type} contains contractions (zero allowed): {bullet_contractions}")

    # 10. PTSD-scope guard
    #
    # Always-blocked: never appropriate in any document regardless of role.
    for term in PTSD_TERMS_ALWAYS_BLOCKED:
        if re.search(rf"\b{re.escape(term)}\b", body, re.IGNORECASE):
            failures.append(f"PTSD-scope violation (always blocked): '{term}' must not appear.")

    # ICAC-gated: blocked by default. Open the gate with allow_icac=True
    # when building documents for child-safety / ICAC platform roles.
    if not allow_icac:
        for term in PTSD_TERMS_ICAC_GATED:
            if re.search(rf"\b{re.escape(term)}\b", body, re.IGNORECASE):
                failures.append(
                    f"PTSD-scope violation (ICAC-gated): '{term}' present. "
                    f"Pass allow_icac=True to permit for child-safety / ICAC role documents."
                )

    # 11. Protected veteran / VEVRAA language guard
    if re.search(r"\b(VEVRAA|protected veteran)\b", body, re.IGNORECASE):
        failures.append("Protected veteran / VEVRAA language present - Troy directed this be omitted.")

    return failures


def scan_pdf(
    pdf_path: str,
    doc_type: str = "resume",
    strict: bool = True,
    allow_icac: bool = False,
) -> list[str]:
    """
    Scan a PDF and return violations.

    Parameters
    ----------
    pdf_path   : path to the PDF file
    doc_type   : "resume" | "cover" | "cv" | "bio"
    strict     : If True (default), raises FailedScan on any violation.
                 If False, prints violations and returns the list.
    allow_icac : When True, opens the ICAC gate - permits CSAM / child-
                 exploitation / ICAC training references. Use only for
                 documents targeting ICAC or child-safety platform roles.
                 All other PTSD-scope terms remain blocked.
    """
    if not Path(pdf_path).exists():
        raise FileNotFoundError(pdf_path)
    text = _extract(pdf_path)
    failures = scan_text(text, doc_type=doc_type, allow_icac=allow_icac)

    name = Path(pdf_path).name
    gate_note = " [ICAC gate: OPEN]" if allow_icac else ""
    if failures:
        msg = (
            f"\n[ANTI-AI SCAN - FAIL] {name}  ({doc_type}){gate_note}\n"
            + "\n".join(f"  * {f}" for f in failures)
        )
        if strict:
            raise FailedScan(msg)
        else:
            print(msg)
    else:
        print(f"[ANTI-AI SCAN - PASS] {name}  ({doc_type}){gate_note}")
    return failures


if __name__ == "__main__":
    # CLI usage:
    #   python anti_ai_scan.py /path/to/file.pdf resume
    #   python anti_ai_scan.py /path/to/file.pdf resume --icac
    p = sys.argv[1]
    t = sys.argv[2] if len(sys.argv) > 2 else "resume"
    icac = "--icac" in sys.argv
    scan_pdf(p, doc_type=t, strict=False, allow_icac=icac)
