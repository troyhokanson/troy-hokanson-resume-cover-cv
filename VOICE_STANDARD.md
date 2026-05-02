# Troy Hokanson Voice Standard

**Permanent. Non-negotiable. Applied to every resume, cover letter, CV, recruiter packet, professional bio, one-pager, or any DOCX/PDF that bears Troy Hokanson's name.**

This file is the canonical source of truth for the voice and anti-AI rules. The local skill (`linkedin-profile-optimizer/SKILL.md`) mirrors it, and the automated scanner (`anti_ai_scan.py`) enforces it on every build. If a document fails the scan, fix the source text and rebuild — never share a document that did not pass.

---

## The Narrator

Every word must read as if Troy wrote it himself. The narrator is:

- 54 years old, Generation X (born 1971)
- Medically retired Minnesota detective with 25 years of sworn service
- Master of Arts, Police Leadership, Administration and Education, University of St. Thomas, GPA 3.94
- 19 years as a remote adjunct faculty member teaching undergraduate Criminal Justice at the University of Phoenix
- Nine-year U.S. Army veteran, honorably discharged
- Trained in the Reid Technique of Interviewing and Interrogation, FBI cell-site analysis, NW3C cybercrime investigation
- Empathetic — 25 years of public service shaped how he writes about victims, fraud impact, and trust

---

## The Voice This Produces

- **Empathetic and humanistic, not corporate or detached.** Fraud is described as something that erodes trust between people and the systems meant to protect them, not as a "loss event" or "risk vector."
- **Plain Gen-X cadence.** Short sentences carry weight. Long sentences carry detail. Mechanical uniformity is an AI tell.
- **Master's-educated precision** — vocabulary is exact, not ornate. Reduced, distilled, identified, documented, examined, traced, established, recovered, obtained. Never elevated, leveraged, harnessed, transformed.
- **Investigations-experienced specificity** — names tools, names dollar amounts, names outcomes, names jurisdictions. Never vague ("handled cases"); always concrete ("led a multi-victim Business Email Compromise investigation that closed with $295,704.11 in court-ordered restitution").
- **Adjunct-faculty clarity** — complex things are made plain, the way Troy explains evidence to a jury or a concept to a 200-level Criminal Justice class. Not academic. Not stiff. Explanatory.
- **Honest framing of skills he is still building.** Working proficiency, building competency, in progress, currently developing through directed self-study. Never overclaim.
- **Closes with one earned, plain sentence.** Never "I look forward to discussing." Never "I'm excited about the opportunity." Closing salutation is always `Respectfully,`.

---

## Three Things Every Cover Letter Must Contain

1. Both law enforcement and military credentials in the first sentence.
2. At least one concrete number or named case outcome from Troy's actual record. Examples:
   - The BEC case: $360,000+ in documented victim losses, $295,704.11 in court-ordered restitution, 15-year federal sentence
   - 5,304 GB of digital evidence processed in 2020
   - Ten partner agencies on the Dakota County Electronic Crimes Task Force
   - 20+ written commendations
   - $3.2M in real estate sales
   - 512 documented hours of investigation-relevant training
3. One sentence of genuine human connection between Troy's public service background and the real-world impact of fraud — fraud raises premiums, denies legitimate claims, takes from people who cannot afford it. Earned, not performed.

## Three Things Every Resume Summary Must Contain

1. "Twenty-five-year medically retired Minnesota detective and digital forensic examiner" or a near-equivalent opener that anchors the reader in his identity.
2. Quantified outcomes from real cases — felony convictions, restitution amounts, federal sentences, partner-agency adoption, training-hours total.
3. Honest tooling positioning — what is mastered (Cellebrite UFED, Magnet AXIOM, FTK, X-Ways, GrayKey, Python, API automation), what is being built (SQL, Tableau, Alteryx), what is in progress (CFE).

---

## Empathy and Humanism Markers (use these — they read as Troy)

- "the trust between people and the systems designed to protect them"
- "the people on the other end of those losses"
- "public service" / "twenty-five years in public service"
- "the work this role calls for is work I have done"
- "writing for audiences who were not there for the investigation"
- references to teaching, training officers, explaining evidence to a jury

## Markers That Violate Troy's Voice (never use)

- **Corporate / SaaS verbs:** leveraged, harnessed, spearheaded, championed, optimized, streamlined, transformed, delivered value, drove outcomes, empowered, elevated, unlocked, seamlessly
- **Detached fraud framing:** "loss vector," "risk surface," "actor," "bad actor," "adversary" as the only descriptor for the people Troy investigated
- **AI throat-clearing:** in today's environment, at the end of the day, needless to say, fundamentally, ultimately, ramping on
- **Performed enthusiasm:** I am excited, I am thrilled, I am eager, I look forward to discussing
- **Overclaim language:** expert in [X], deep expertise in [X] when Troy is actually building competency
- **Marketing-department openers:** "As a [title]...", "I bring", "I offer", "With over 25 years of experience..."

---

## Punctuation Rules (highest-signal AI tells)

| Punctuation | Rule |
|---|---|
| Em dash (—) | Never. Anywhere. Replace with a period or restructure. |
| En dash (–) | Never in prose. Plain hyphen acceptable in date fields (1998-2024). |
| Semicolon (;) | Never in cover letters or About / bio sections. Acceptable in resume bullets between parallel items. |
| Ellipsis (...) | Never. Use a period or rewrite. |
| Exclamation point (!) | Never in any professional content. Zero exceptions. |
| Curly / smart quotes (" ' ' ') | Never. Use straight quotes only. |
| Oxford comma | Use naturally, not mechanically. Mechanical consistency is itself an AI signal. |

---

## Number Conventions

- One through nine: spell out (four cases, nine interviews)
- 10 and above: numerals (25 years, 14 cases, $47,000)
- Statistics, case counts, technical measurements: always numerals regardless of size

---

## Contractions

- Resume / CV bullets: zero contractions. Always.
- Cover letters: maximum two contractions in the entire document. Prefer the uncontracted form.
- Possessives like "Master's degree" or "Comcast's customers" are not contractions and are fine.

---

## Closing

Cover letters always close with exactly:

```
Respectfully,
[48pt blank space for digital signature]
Troy Hokanson
```

Never use Sincerely, Best regards, Best, Thank you, Kind regards, or any other closing.

---

## Automatic Enforcement

This standard is enforced by [`anti_ai_scan.py`](./anti_ai_scan.py), called at the bottom of every `build_*.py` script:

```python
from templates.anti_ai_scan import scan_pdf
scan_pdf(PDF, doc_type="resume")   # or "cover" / "cv" / "bio"
```

The scanner raises `FailedScan` and hard-blocks the build on any violation. Manual self-review is still required after the scan passes — the scanner catches phrases, but it cannot catch tone. Read the document out loud once before sharing.

---

## When to Update This File

Update this file when:

1. A new AI-flagged phrase is caught by ZeroGPT / Copyleaks / Grammarly during real submission review
2. Troy provides feedback that a document did not sound like him
3. A new voice marker (empathetic phrase, narrative anchor) proves effective in a successful application
4. The narrator facts change (age, retirement status, certifications, education)

Always update the canonical phrase list in `anti_ai_scan.py` (`FORBIDDEN_PHRASES` or `EXTRA_FLAGGED`) at the same time so the rule is enforced automatically.
