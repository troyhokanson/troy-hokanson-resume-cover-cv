# Troy Hokanson — Document Header Standard

**Locked April 2026. This is the single source of truth for every document Troy ships.**

Any resume, cover letter, CV, portfolio export, VA tracker print view, or other artifact bearing Troy's name MUST use the locked header from this repo. No exceptions. No hand-rolled headers. No "just this once" deviations.

---

## Trigger Keywords (auto-route to this standard)

If the user request contains ANY of the following words/phrases, you MUST use this header standard. No matter which skill is active, no matter how the request is phrased.

**Document type triggers:**
resume, résumé, cv, curriculum vitae, cover letter, coverletter, application package, application docs, application materials, job package, application bundle, applicant materials, hiring packet, recruiter packet, intro letter, letter of interest, letter of intent, professional bio, biographical statement, statement of interest, candidate profile pdf, candidate profile doc, profile sheet, one-pager, leave-behind, attach my resume, send my resume, polish my resume, format my resume

**File format triggers:**
docx, .docx, word doc, word document, microsoft word, pdf, .pdf, adobe pdf, export pdf, save as pdf, save as word, print to pdf, save as docx, page header, document header, header bar, header banner, navy header, navy bar, gold rule, gold underline, contact row, contact bar, name header

**Action triggers:**
tailor a resume, tailor a cover letter, build a resume, build a cover letter, build a cv, generate a resume, generate a cover letter, generate a cv, write me a resume, write me a cover letter, draft a resume, draft a cover letter, draft a cv, customize my resume, customize my cover letter, rebuild the resume, rebuild the cover letter, redo the header, fix the header, format the header, fix the formatting, polish the formatting, match the template, match the brand, apply the template, apply the brand, use the standard header, use my standard, use my locked header, use the locked template, the standard one, the usual format, the same look, the brand look, navy and gold, navy + gold, navy/gold

**Format auto-routing:**

| Phrase the user says | Format to build | Module to import |
|---|---|---|
| "docx", "Word doc", "editable", "send to recruiter as Word" | DOCX | `templates.docx_header` |
| "pdf", "final", "polished", "locked version", "to upload", "for the application" | PDF | `templates.pdf_header` |
| "both", "package", "bundle", "application package", "resume + cover letter" | DOCX **and** PDF | both modules |
| Format not specified | DOCX (editable) by default; ask if PDF is also needed | `templates.docx_header` |

**If unsure which module to use, default to DOCX. Never hand-roll either format.**

---

## The Standard

| Element | Spec |
|---|---|
| Background | Full-bleed navy `#0D1B2A`, zero whitespace above, left, or right |
| Name | "Troy J. Hokanson", Garamond-Bold 28pt, WHITE `#FFFFFF`, centered |
| Rule | Thin gold `#C9A84C`, 0.75pt, centered, ~70% page width |
| Contact row | Inter 9pt (PDF) / Calibri 10pt (DOCX), gold `#C9A84C`, centered, separator `   \|   ` |
| Contact items | Loaded from environment variables via `config.py` — see `config.example.env`. Never hardcoded. |
| Subtitle | NONE. No role title between name and contact row. Ever. |
| Page 2+ (PDF) | Slim 0.42" navy bar with name only in white Garamond-Bold 14pt |
| Page 2+ (DOCX) | Same banner repeats via section header part |
| Body top margin | 1.55" page 1 / 0.67" page 2+ (matches `MARGIN['top_page1']` / `MARGIN['top_pageN']`) |

## How to Use

### DOCX (resumes, cover letters, CVs in Word format)

```python
import sys
sys.path.insert(0, "/home/user/workspace")
from templates.docx_header import (
    new_document, build_navy_header,
    add_section_heading, add_bullet, add_job_block,
)

doc = new_document()
build_navy_header(doc)
add_section_heading(doc, "Professional Summary")
# ... body ...
doc.save("output.docx")
```

### PDF (resumes, cover letters, CVs in PDF format — ReportLab Platypus)

```python
import sys
sys.path.insert(0, "/home/user/workspace")
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate
from templates.pdf_header import draw_page1_header, draw_pageN_header, MARGIN, clean_pdf_metadata

def on_first(c, d): draw_page1_header(c, LETTER)
def on_later(c, d): draw_pageN_header(c, LETTER)

doc = SimpleDocTemplate(
    out_path, pagesize=LETTER,
    leftMargin=MARGIN["left"], rightMargin=MARGIN["right"],
    topMargin=0, bottomMargin=MARGIN["bottom"],
)
doc.build(story, onFirstPage=on_first, onLaterPages=on_later)
clean_pdf_metadata(out_path, title="Resume - Troy Hokanson")
```

### PDF (direct canvas — for non-Platypus exports)

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from templates.pdf_header import draw_page1_header

c = canvas.Canvas("out.pdf", pagesize=LETTER)
draw_page1_header(c, LETTER)
# ... draw body content below MARGIN['top_page1'] ...
c.save()
```

## Visual Ground Truth

`templates/reference_header.docx` — open this and any new doc side by side. Page 1 must match. If it doesn't, the build script is wrong, not the module.

Rebuild the reference after any module change:

```bash
cd /home/user/workspace && python3 templates/build_reference.py
```

## Hard Rules

1. **Never hand-roll the header.** Always import from `templates.docx_header` or `templates.pdf_header`.
2. **Never add a subtitle, role title, eyebrow, or tagline between the name and contact row.** The contact row sits directly under the gold rule.
3. **Never use Inter for the name** or Garamond for the body.
4. **Never use em dashes, en dashes, exclamation points, or VEVRAA language** anywhere in the document.
5. **Never use `topMargin > 0` on a PDF** — the navy banner must sit flush at the top.
6. **If the spec genuinely needs to change**, edit both `docx_header.py` and `pdf_header.py`, rebuild the reference DOCX, bump the version, and commit.

## Repo

Public repo: https://github.com/troyhokanson/troy-hokanson-resume-cover-cv

Pull into a fresh sandbox:

```bash
git clone https://github.com/troyhokanson/troy-hokanson-resume-cover-cv
cd troy-hokanson-resume-cover-cv
cp config.example.env .env
# Edit .env and fill in your real contact values
```

## Contact Info Setup (Multi-Device)

Contact details (phone, email, location) are loaded from environment variables — never hardcoded in the public repo.

**Local machine (any device):**
1. Copy `config.example.env` to `.env` in the repo root
2. Fill in your real values
3. The `.env` file is gitignored and will never be committed

**GitHub Actions (automated builds):**
Add these secrets under Settings -> Secrets and variables -> Actions:
- `TROY_PHONE` — e.g. `612.555.0000`
- `TROY_EMAIL` — e.g. `TroyHokanson@iCloud.com`
- `TROY_LOCATION` — e.g. `Lakeville, MN`
- `TROY_LINKEDIN` — e.g. `linkedin.com/in/troyhokanson`
- `TROY_PORTFOLIO` — e.g. `https://troy-hokanson.github.io/portfolio`

Builds run on any device or via Actions will inject the real values into every document header automatically.

## Skill Enforcement

These skills enforce the standard at the top of their instructions and must never be bypassed:

- `linkedin-profile-optimizer` (resumes, cover letters, CVs, LinkedIn-adjacent docs)
- `investigator-portfolio-website-optimizer` (printable case-study exports, portfolio PDFs)
- `resume-file-router` (validation gate before OneDrive export)
- `va-disability-tracker` (any printable claim-package artifact)

If you're working in any of these skills and you're tempted to write header code from scratch, stop and import from this repo instead.
