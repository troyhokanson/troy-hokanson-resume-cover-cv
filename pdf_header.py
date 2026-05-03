"""
Troy J. Hokanson — Locked PDF Header Module
============================================

SINGLE SOURCE OF TRUTH for the navy/gold header on every PDF resume,
cover letter, CV, or any other PDF artifact bearing Troy's name.

Matches the locked DOCX spec in templates/docx_header.py exactly:

  - Full-bleed navy #0D1B2A bar, ZERO whitespace above/left/right
  - "Troy J. Hokanson" in WHITE Garamond-Bold ~28pt, centered
  - Thin gold #C9A84C horizontal rule beneath the name
  - Gold contact row, Inter ~9pt, pipe-separated, centered
  - NO subtitle / role title between name and contact row
  - Page 2+ on resume/CV: slim navy bar with name only

Usage in any ReportLab build script:

    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import LETTER
    from templates.pdf_header import draw_page1_header, draw_pageN_header, BRAND, MARGIN

    c = canvas.Canvas(out_path, pagesize=LETTER)
    draw_page1_header(c, LETTER)
    # ... draw body ...
    c.showPage()
    draw_pageN_header(c, LETTER)
    # ... etc

For Platypus (SimpleDocTemplate), pass these as canvas-level onPage callbacks:

    def on_first(c, d): draw_page1_header(c, LETTER)
    def on_later(c, d): draw_pageN_header(c, LETTER)
    doc = SimpleDocTemplate(..., topMargin=0)
    doc.build(story, onFirstPage=on_first, onLaterPages=on_later)

DO NOT hand-roll the header in build scripts. If the locked spec needs to
change, change BOTH this module AND templates/docx_header.py and bump
the templates repo version.

Locked April 2026.
"""

from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from config import TROY_NAME, TROY_PHONE, TROY_EMAIL, TROY_LOCATION, TROY_LINKEDIN, TROY_PORTFOLIO


# ============================================================
# BRAND CONSTANTS — keep aligned with templates/docx_header.py
# ============================================================

BRAND = {
    "navy": HexColor("#0D1B2A"),
    "gold": HexColor("#C9A84C"),
    "steel": HexColor("#2D6A9F"),
    "white": white,
    "black": HexColor("#141414"),
    "gray": HexColor("#555555"),
}

NAME = TROY_NAME
# Contact info loaded from environment variables via config.py.
# Set values in .env (local) or GitHub Actions Secrets (CI). See config.example.env.
_phone_digits = TROY_PHONE.replace(".", "").replace("-", "").replace(" ", "")
CONTACT_PARTS = [
    TROY_LOCATION,
    *( [TROY_PHONE] if TROY_PHONE else [] ),
    TROY_EMAIL,
    TROY_LINKEDIN,
    "Investigative Portfolio",
]
CONTACT_LINKS = {
    **( {TROY_PHONE: f"tel:+1{_phone_digits}"} if TROY_PHONE else {} ),
    TROY_EMAIL: f"mailto:{TROY_EMAIL}",
    TROY_LINKEDIN: f"https://www.{TROY_LINKEDIN}" if not TROY_LINKEDIN.startswith("http") else TROY_LINKEDIN,
    "Investigative Portfolio": TROY_PORTFOLIO,
}

# Locked margins — use these on every doc so headers + body align
MARGIN = {
    "left": 0.6 * inch,
    "right": 0.6 * inch,
    "top_page1": 1.55 * inch,   # body starts below the page-1 banner
    "top_pageN": 0.67 * inch,   # body starts below the slim page-2+ bar
    "bottom": 0.55 * inch,
}

PAGE1_BANNER_HEIGHT = 1.45 * inch   # tall navy banner with name + rule + contact
PAGEN_BANNER_HEIGHT = 0.42 * inch   # slim navy bar with name only
SEPARATOR = "   |   "


# ============================================================
# FONT REGISTRATION
# ============================================================

_FONTS_REGISTERED = False

def _register_fonts():
    """Register Garamond-Bold and Inter; fall back gracefully if missing."""
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return

    # Try common font paths; ReportLab will fall back to Helvetica if not found
    candidates = {
        "Garamond-Bold": [
            "/usr/share/fonts/truetype/ebgaramond/EBGaramond-Bold.ttf",
            "/usr/share/fonts/ebgaramond/EBGaramond-Bold.ttf",
            "/home/user/workspace/templates/fonts/EBGaramond-Bold.ttf",
        ],
        "Inter": [
            "/usr/share/fonts/truetype/inter/Inter-Regular.ttf",
            "/usr/share/fonts/inter/Inter-Regular.ttf",
            "/home/user/workspace/templates/fonts/Inter-Regular.ttf",
        ],
        "Inter-Bold": [
            "/usr/share/fonts/truetype/inter/Inter-Bold.ttf",
            "/usr/share/fonts/inter/Inter-Bold.ttf",
            "/home/user/workspace/templates/fonts/Inter-Bold.ttf",
        ],
        "Inter-Italic": [
            "/usr/share/fonts/truetype/inter/Inter-Italic.ttf",
            "/home/user/workspace/templates/fonts/Inter-Italic.ttf",
        ],
    }
    for name, paths in candidates.items():
        for p in paths:
            if os.path.exists(p):
                try:
                    pdfmetrics.registerFont(TTFont(name, p))
                    break
                except Exception:
                    pass
    _FONTS_REGISTERED = True


def _safe_font(preferred, fallback):
    """Return the preferred font if registered, else the fallback."""
    try:
        pdfmetrics.getFont(preferred)
        return preferred
    except Exception:
        return fallback


# ============================================================
# DRAW FUNCTIONS
# ============================================================

def draw_page1_header(c, pagesize, *, name=NAME, contact_parts=CONTACT_PARTS,
                      contact_links=None):
    """
    Draw the full page-1 banner: navy block, white name, gold rule, gold contact row.

    Call this from onFirstPage in Platypus, or directly after creating the canvas.
    Doc must be built with topMargin=0 so the banner sits flush.
    """
    _register_fonts()
    if contact_links is None:
        contact_links = CONTACT_LINKS

    page_w, page_h = pagesize
    band_h = PAGE1_BANNER_HEIGHT
    band_y = page_h - band_h

    # 1. Full-bleed navy block (extends a hair past edges to kill rounding gaps)
    c.setFillColor(BRAND["navy"])
    c.rect(-0.05 * inch, band_y - 0.05 * inch,
           page_w + 0.1 * inch, band_h + 0.1 * inch, fill=1, stroke=0)

    # 2. Name — WHITE Garamond-Bold 28pt, centered
    name_font = _safe_font("Garamond-Bold", "Helvetica-Bold")
    c.setFillColor(BRAND["white"])
    c.setFont(name_font, 28)
    name_y = band_y + band_h - 0.55 * inch
    c.drawCentredString(page_w / 2, name_y, name)

    # 3. Thin gold rule beneath the name (centered, ~70% of page width)
    c.setStrokeColor(BRAND["gold"])
    c.setLineWidth(0.75)
    rule_y = name_y - 0.18 * inch
    rule_inset = page_w * 0.15
    c.line(rule_inset, rule_y, page_w - rule_inset, rule_y)

    # 4. Contact row — Inter 9pt, gold, centered, pipe-separated
    body_font = _safe_font("Inter", "Helvetica")
    c.setFillColor(BRAND["gold"])
    c.setFont(body_font, 9)

    contact_text = SEPARATOR.join(contact_parts)
    text_w = c.stringWidth(contact_text, body_font, 9)
    contact_y = rule_y - 0.25 * inch
    start_x = (page_w - text_w) / 2
    c.drawString(start_x, contact_y, contact_text)

    # 5. Add clickable link rectangles for each linkable contact part
    cursor_x = start_x
    sep_w = c.stringWidth(SEPARATOR, body_font, 9)
    for i, part in enumerate(contact_parts):
        part_w = c.stringWidth(part, body_font, 9)
        url = contact_links.get(part)
        if url:
            c.linkURL(
                url,
                (cursor_x, contact_y - 2, cursor_x + part_w, contact_y + 10),
                relative=0,
            )
        cursor_x += part_w
        if i < len(contact_parts) - 1:
            cursor_x += sep_w


def draw_pageN_header(c, pagesize, *, name=NAME):
    """
    Draw the slim page-2+ bar: thin navy strip with the name only.

    Call from onLaterPages in Platypus. Use MARGIN['top_pageN'] for body start.
    """
    _register_fonts()
    page_w, page_h = pagesize
    band_h = PAGEN_BANNER_HEIGHT
    band_y = page_h - band_h

    c.setFillColor(BRAND["navy"])
    c.rect(-0.05 * inch, band_y - 0.05 * inch,
           page_w + 0.1 * inch, band_h + 0.1 * inch, fill=1, stroke=0)

    name_font = _safe_font("Garamond-Bold", "Helvetica-Bold")
    c.setFillColor(BRAND["white"])
    c.setFont(name_font, 14)
    c.drawCentredString(page_w / 2, band_y + band_h / 2 - 5, name)


def clean_pdf_metadata(path, *, title="", subject="", keywords=""):
    """
    Strip ReportLab/Perplexity/Claude/etc fingerprints from a finished PDF.
    Sets Author=Troy Hokanson, Creator=Adobe Acrobat Pro, Producer="".
    """
    try:
        import pypdf
    except ImportError:
        return  # silently skip if pypdf not installed

    reader = pypdf.PdfReader(path)
    writer = pypdf.PdfWriter(clone_from=reader)
    writer.add_metadata({
        "/Author": "Troy Hokanson",
        "/Creator": "Adobe Acrobat Pro",
        "/Producer": "",
        "/Title": title or "",
        "/Subject": subject or "",
        "/Keywords": keywords or "",
    })
    with open(path, "wb") as fh:
        writer.write(fh)


__all__ = [
    "BRAND", "NAME", "CONTACT_PARTS", "CONTACT_LINKS", "MARGIN",
    "PAGE1_BANNER_HEIGHT", "PAGEN_BANNER_HEIGHT",
    "draw_page1_header", "draw_pageN_header",
    "clean_pdf_metadata",
]
