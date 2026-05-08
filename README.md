# Troy Hokanson — Document Templates for Investigative Job Search - Microsoft Word or PDF Format.

**SINGLE SOURCE OF TRUTH** for every Troy Hokanson resume, cover letter, CV, recruiter packet, professional bio, one-pager, or any DOCX/PDF document bearing his name. This repo MUST be cloned into `/home/user/workspace/templates/` (via symlink) at the start of every application build session — automatically, no exceptions.

This repo enforces three locked standards:

1. **Navy/gold header layout** (HEADER_STANDARD.md, docx_header.py, pdf_header.py)
2. **Anti-AI / voice rules** (VOICE_STANDARD.md, anti_ai_scan.py)
3. **PTSD-safe scope and writing voice** (linked from VOICE_STANDARD.md)

If you are about to build a Hokanson document and this repo is not present in the workspace, STOP and clone it first.

---

## Repository Structure

```
troy-hokanson-resume-cover-cv/
├── config.py               # Contact info loader — reads env vars, never hardcoded
├── config.example.env      # Copy to .env and fill in real values
├── docx_header.py          # Locked DOCX header builder + body helpers
├── pdf_header.py           # Locked PDF page-1 header renderer
├── anti_ai_scan.py         # Automatic voice/anti-AI enforcement gate
├── build_reference.py      # Rebuilds reference_header.docx after any header change
├── reference_header.docx   # Visual ground truth — diff against every new build
├── requirements.txt        # Python dependencies
├── fonts/
│   └── README.md           # Font installation guide (EB Garamond, Inter)
├── tests/
│   ├── test_anti_ai_scan.py  # 80+ unit tests for every scan rule
│   └── test_config.py        # Tests for env-var loading and safe fallbacks
├── HEADER_STANDARD.md      # Locked layout specification
├── VOICE_STANDARD.md       # Troy's permanent voice standard
├── SYSTEM_PROMPT.md        # Copy-paste system prompt for custom AI setups
├── PLATFORM_SETUP.md       # How to configure ChatGPT, Claude, Gemini, etc.
└── chatgpt_action_schema.json  # OpenAPI schema for ChatGPT Actions
```

---

## Quick Start

```bash
# 1. Clone and set up
git clone https://github.com/troyhokanson/troy-hokanson-resume-cover-cv
cd troy-hokanson-resume-cover-cv
pip install -r requirements.txt

# 2. Configure contact info (never hardcoded — kept out of the repo)
cp config.example.env .env
# Edit .env and fill in real values

# 3. Verify imports work
python -c "from docx_header import build_navy_header, new_document; print('OK')"
python -c "from pdf_header import draw_page1_header; print('OK')"
python -c "from anti_ai_scan import scan_pdf; print('OK')"

# 4. Run the test suite
python -m pytest tests/ -v

# 5. Build the visual reference DOCX
python build_reference.py
```

---

## Usage in a build script

```python
import sys
sys.path.insert(0, "/home/user/workspace")
from templates.docx_header import (
    new_document, build_navy_header,
    add_section_heading, add_bullet, add_job_block,
    set_run, set_paragraph_format,
    BODY_FONT, NAME_FONT, NAVY, GOLD, STEEL, BLACK, GRAY, WHITE,
)

doc = new_document()
build_navy_header(doc)
add_section_heading(doc, "Professional Summary")
# ... body content using add_bullet, add_job_block, etc.
doc.save("/home/user/workspace/output/Hokanson_Resume_Employer_Role.docx")

# Convert to PDF, then run the MANDATORY anti-AI / voice scan
import subprocess
subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", "/home/user/workspace/output",
                "/home/user/workspace/output/Hokanson_Resume_Employer_Role.docx"],
               check=True, capture_output=True)

from templates.anti_ai_scan import scan_pdf
scan_pdf("/home/user/workspace/output/Hokanson_Resume_Employer_Role.pdf",
         doc_type="resume")   # raises FailedScan if any violation
```

**Every `build_*.py` script must end with the `scan_pdf` call.** Skipping the scan is not allowed.

---

## Files

- `docx_header.py` — the locked header builder + shared body helpers. Import this in every build script. Never hand-roll the header.
- `pdf_header.py` — locked PDF page-1 header renderer.
- `reference_header.docx` — visual ground truth. Diff against page 1 of every new build.
- `build_reference.py` — rebuilds the reference DOCX after any header change.
- `HEADER_STANDARD.md` — locked layout specification.
- `anti_ai_scan.py` — **automatic enforcement** of the voice and anti-AI rules. Called at the bottom of every `build_*.py` script. Hard-blocks any document that fails.
- `VOICE_STANDARD.md` — Troy's permanent voice standard (54-year-old Gen-X retired detective, Master's-educated, empathetic / humanistic, investigations-experienced).
- `requirements.txt` — Python dependencies. Install with `pip install -r requirements.txt`.
- `fonts/README.md` — Instructions for installing EB Garamond and Inter fonts locally.
- `tests/` — Unit tests for the scan engine and config loader. Run with `python -m pytest tests/ -v`.

---

## Locked spec (matches UHG reference April 2026)

- Full-bleed navy `#0D1B2A` bar, ZERO whitespace above (sits in section page header part)
- `Troy J. Hokanson` in WHITE Garamond-Bold ~28pt, mixed case, centered
- INSET gold `#C9A84C` horizontal rule (not edge-to-edge)
- Single gold contact row beneath, pipe-separated
- NO subtitle / role title between name and contact row
- Section headings: steel-blue `#2D6A9F` with gold underline rule

---

## Contact Info Setup (Multi-Device)

Contact details (phone, email, location) are **never hardcoded** in this repo. They are loaded from environment variables at build time.

**Local machine (any device):**
1. Copy `config.example.env` to `.env` in the repo root: `cp config.example.env .env`
2. Fill in your real values — the `.env` file is gitignored and will never be committed
3. Run any build script normally; `config.py` loads `.env` automatically

**GitHub Actions (automated builds):**
Add these secrets under Settings → Secrets and variables → Actions:
- `TROY_PHONE` — e.g. `612.352.8647`
- `TROY_EMAIL` — e.g. `TroyHokanson@iCloud.com`
- `TROY_LOCATION` — e.g. `Lakeville, MN`
- `TROY_LINKEDIN` — e.g. `linkedin.com/in/troyhokanson`
- `TROY_PORTFOLIO` — e.g. `https://troy-hokanson.github.io/portfolio`

---

## To pull into a fresh sandbox (AUTOMATIC at session start)

```bash
cd /home/user/workspace
gh repo clone troyhokanson/troy-hokanson-resume-cover-cv
ln -sfn /home/user/workspace/troy-hokanson-resume-cover-cv /home/user/workspace/templates
pip install -r templates/requirements.txt
```

After clone, verify imports work:
```python
from templates.docx_header import build_navy_header, new_document
from templates.pdf_header import draw_page1_header
from templates.anti_ai_scan import scan_pdf
```

---

## Running Tests

```bash
# From the repo root (no symlink needed — tests import directly)
python -m pytest tests/ -v

# From the workspace root (templates/ symlink layout)
python -m pytest templates/tests/ -v
```

Tests cover:
- All 50+ forbidden phrases and extra-flagged AI clichés
- All punctuation rules (em dash, en dash, exclamation, ellipsis, curly quotes)
- Cover-letter structural rules (closing, contraction cap, semicolons)
- Resume/CV contraction rules
- PTSD-scope guard
- VEVRAA language guard
- Config env-var loading and safe fallbacks

---

## Changing the locked spec

If the header style genuinely needs to change:
1. Edit `docx_header.py`
2. Run `python3 build_reference.py` to rebuild the reference
3. Visually diff against the prior reference
4. Run the test suite: `python -m pytest tests/ -v`
5. Commit and push: `git add -A && git commit -m "Header change: <reason>" && git push`
