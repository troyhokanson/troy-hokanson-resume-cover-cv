# Troy Hokanson — Document Templates for Investigative Job Search - Microsoft Word or PDF Format.

**SINGLE SOURCE OF TRUTH** for every Troy Hokanson resume, cover letter, CV, recruiter packet, professional bio, one-pager, or any DOCX/PDF document bearing his name. This repo MUST be cloned into `/home/user/workspace/templates/` (via symlink) at the start of every application build session — automatically, no exceptions.

This repo enforces three locked standards:

1. **Navy/gold header layout** (HEADER_STANDARD.md, docx_header.py, pdf_header.py)
2. **Anti-AI / voice rules** (VOICE_STANDARD.md, anti_ai_scan.py)
3. **PTSD-safe scope and writing voice** (linked from VOICE_STANDARD.md)

If you are about to build a Hokanson document and this repo is not present in the workspace, STOP and clone it first.

## Files
- `docx_header.py` — the locked header builder + shared body helpers. Import this in every build script. Never hand-roll the header.
- `pdf_header.py` — locked PDF page-1 header renderer.
- `reference_header.docx` — visual ground truth. Diff against page 1 of every new build.
- `build_reference.py` — rebuilds the reference DOCX after any header change.
- `HEADER_STANDARD.md` — locked layout specification.
- `anti_ai_scan.py` — **automatic enforcement** of the voice and anti-AI rules. Called at the bottom of every `build_*.py` script. Hard-blocks any document that fails.
- `VOICE_STANDARD.md` — Troy's permanent voice standard (54-year-old Gen-X retired detective, Master's-educated, empathetic / humanistic, investigations-experienced).

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

## Locked spec (matches UHG reference April 2026)

- Full-bleed navy `#0D1B2A` bar, ZERO whitespace above (sits in section page header part)
- `Troy J. Hokanson` in WHITE Garamond-Bold ~28pt, mixed case, centered
- INSET gold `#C9A84C` horizontal rule (not edge-to-edge)
- Single gold contact row beneath, pipe-separated
- NO subtitle / role title between name and contact row
- Section headings: steel-blue `#2D6A9F` with gold underline rule

## To pull into a fresh sandbox (AUTOMATIC at session start)

```bash
cd /home/user/workspace
gh repo clone troy-hokanson-kw-475/troy-hokanson-resume-cover-cv  # use api_credentials=["github"]
ln -sfn /home/user/workspace/troy-hokanson-resume-cover-cv /home/user/workspace/templates
```

After clone, verify imports work:
```python
from templates.docx_header import build_navy_header, new_document
from templates.pdf_header import draw_page1_header
from templates.anti_ai_scan import scan_pdf
```

## Changing the locked spec

If the header style genuinely needs to change:
1. Edit `docx_header.py`
2. Run `python3 build_reference.py` to rebuild the reference
3. Visually diff against the prior reference
4. Commit and push: `git add -A && git commit -m "Header change: <reason>" && git push`
