# Troy Hokanson — DOCX Node.js Formatting Standard

**Locked May 2026. Single source of truth for Word documents built with the Node.js docx npm library.**

This companion to HEADER_STANDARD.md covers the Node.js / docx@8+ implementation specifically.
The Python (python-docx) standard remains in HEADER_STANDARD.md.

---

## Colors

| Token  | Hex     | Use                          |
|--------|---------|------------------------------|
| NAVY   | 1C2B4A  | Header background, section headers, subheads |
| GOLD   | C09A20  | Gold rule, bullet character, job titles, table borders |
| WHITE  | FFFFFF  | Header name and contact text |
| BLACK  | 000000  | Body text, employer names    |

Font: **Garamond** throughout all elements — no exceptions.

---

## Font Sizes (half-points)

`javascript
const SZ_NAME     = 84;   // 42pt  — header name
const SZ_CONTACT  = 28;   // 14pt  — contact line in header
const SZ_SUBTITLE = 20;   // 10pt  — cover letter subtitle only
const SZ_SECHEAD  = 36;   // 18pt  — section headers
const SZ_JOBTITLE = 30;   // 15pt  — job titles (gold italic bold)
const SZ_BODY     = 24;   // 12pt  — body text and bullets
const SZ_SKILLS   = 18;   //  9pt  — competency/skills table cells
const SZ_RUNHEAD  = 44;   // 22pt  — running header pages 2+
const SZ_SUBHEAD  = 28;   // 14pt  — CV sub-section labels
`

> **SZ_BODY must be 24 (12pt).** Values of 38 (19pt) or higher produce oversized body text.

---

## Page Geometry (DXA / twips)

`javascript
const PAGE_W    = 12240;
const LM        = 1440;               // left & right margin (1 inch)
const CONTENT_W = PAGE_W - 2 * LM;   // 9360 DXA
`

---

## Section Margins

`javascript
const SEC1_MARGIN = { top: 0,    right: LM, bottom: 1008, left: LM }; // page 1
const SEC2_MARGIN = { top: 1200, right: LM, bottom: 1008, left: LM }; // pages 2+
`

Page 1 	op: 0 is required — the navy header table must sit flush at the top of the page.

---

## Full-Bleed Navy Header (Page 1)

Use a negative left indent equal to LM to extend the table beyond the page margin:

`javascript
return new Table({
  width:  { size: PAGE_W, type: WidthType.DXA },
  indent: { size: -LM,   type: WidthType.DXA },  // negative = full-bleed
  layout: TableLayoutType.FIXED,
  borders: NB,
  rows,
});
`

Running header (pages 2+) uses the same negative indent, placed in the Word header zone via 
ew Header({ children: [table] }).

---

## Skills / Competency Table

**Full content width, no left indent.** A non-zero indent creates a blank gap on the left side.

`javascript
return new Table({
  width:  { size: CONTENT_W, type: WidthType.DXA },
  indent: { size: 0,         type: WidthType.DXA },  // must be 0
  layout: TableLayoutType.FIXED,
  borders: NB,
  rows,
});
`

---

## Orphan Prevention — keepNext

The following paragraph types MUST include keepNext: true to prevent section headers and job titles from appearing alone at the bottom of a page:

`javascript
function secHead(text) {
  return new Paragraph({
    keepNext: true,
    // ...
  });
}

function jobTitle(text) {
  return new Paragraph({
    keepNext: true,
    // ...
  });
}

function empLine(company, dates) {
  return new Paragraph({
    keepNext: true,
    // ...
  });
}
`

keepNext: true on mpLine is also required — without it the employer line can orphan even when jobTitle is chained correctly.

---

## Gold Bullet Character

Defined via numbering config, not a text character:

`javascript
const numbering = {
  config: [{
    reference: 'bullets',
    levels: [{
      level: 0,
      format: LevelFormat.BULLET,
      text: '•',
      alignment: AlignmentType.LEFT,
      style: {
        paragraph: { indent: { left: 360, hanging: 180 } },
        run: { size: SZ_BODY, font: 'Garamond', color: 'C09A20' },
      },
    }],
  }],
};
`

---

## Education Lines

The duLine() helper accepts an optional fifth honors parameter:

`javascript
function eduLine(degree, school, year, gpa, honors) {
  const schoolLine = school + '   |   ' + year + '   |   GPA ' + gpa
    + (honors ? '   |   ' + honors : '');
  return [
    new Paragraph({ children: [new TextRun({ text: degree, bold: true, ... })], keepNext: true }),
    new Paragraph({ children: [new TextRun({ text: schoolLine, ... })] }),
  ];
}
`

Always pass city/state in the school string: 'St. Cloud State University, St. Cloud, MN'.

---

## Hard Rules

1. SZ_BODY = 24 (12pt). Never 38 or higher.
2. Skills tables: indent: { size: 0 }. Never a positive indent.
3. secHead, jobTitle, and mpLine must all include keepNext: true.
4. Page 1 section margin: 	op: 0. Required for full-bleed header.
5. Honors (Magna Cum Laude, etc.) go in the duLine fifth parameter — never omitted.
6. City/state always included in school name string.
7. All dates written in full: 'March 2010 – May 2011', not '2010-2011'.

---

## Reference Implementation

uild_roblox.js (Roblox CHIIOPS application, May 2026) is the canonical corrected Node.js build script demonstrating all of these standards.

---

## Repo

https://github.com/troyhokanson/troy-hokanson-resume-cover-cv
