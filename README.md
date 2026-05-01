# Troy Hokanson — Document Templates for Investigative Job Search - Microsoft Word or PDF Format.

Locked source of truth for the navy/gold header used on every DOCX resume, cover letter, and CV.

## Files
- `docx_header.py` — the locked header builder + shared body helpers. Import this in every build script. Never hand-roll the header.
- `reference_header.docx` — visual ground truth. Diff against page 1 of every new build.
- `build_reference.py` — rebuilds the reference DOCX after any header change.

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
doc.save("/home/user/workspace/Hokanson_Resume_Employer_Role.docx")
```

## Locked spec (matches UHG reference April 2026)

- Full-bleed navy `#0D1B2A` bar, ZERO whitespace above (sits in section page header part)
- `Troy J. Hokanson` in WHITE Garamond-Bold ~28pt, mixed case, centered
- INSET gold `#C9A84C` horizontal rule (not edge-to-edge)
- Single gold contact row beneath, pipe-separated
- NO subtitle / role title between name and contact row
- Section headings: steel-blue `#2D6A9F` with gold underline rule

## To pull into a fresh sandbox

```
cd /home/user/workspace
git clone https://github.com/troy-hokanson-kw-475/troy-hokanson-resume-cover-cv

```

## Changing the locked spec

If the header style genuinely needs to change:
1. Edit `docx_header.py`
2. Run `python3 build_reference.py` to rebuild the reference
3. Visually diff against the prior reference
4. Commit and push: `git add -A && git commit -m "Header change: <reason>" && git push`
