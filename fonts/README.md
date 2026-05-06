# fonts/ — Optional Local Font Overrides

`pdf_header.py` searches this directory for fonts before falling back to
system paths and then to Helvetica (ReportLab built-in). Placing fonts here
is optional but ensures consistent rendering across devices.

## Fonts used

| Font name in code | File expected here |
|---|---|
| `Garamond-Bold` | `EBGaramond-Bold.ttf` |
| `Inter` | `Inter-Regular.ttf` |
| `Inter-Bold` | `Inter-Bold.ttf` |
| `Inter-Italic` | `Inter-Italic.ttf` |

## Where to get them

### EB Garamond (open-source, SIL OFL license)
Download from Google Fonts or the official release:

```
https://github.com/octaviopardo/EBGaramond12/releases
```

Save `EBGaramond-Bold.ttf` into this `fonts/` directory.

### Inter (open-source, SIL OFL license)
Download from the official release:

```
https://github.com/rsms/inter/releases
```

Save `Inter-Regular.ttf`, `Inter-Bold.ttf`, and `Inter-Italic.ttf`
into this `fonts/` directory.

## Why these are not committed

Font files are binary, often several MB each, and are covered by separate
open-source licenses (SIL OFL). Committing them would bloat the repo history.
The `.gitignore` excludes `*.ttf` and `*.otf` from this directory.

## Fallback behavior

If a font file is not found here or at a system path, `pdf_header.py`
silently falls back to ReportLab's built-in Helvetica family. Documents
will still build and pass the anti-AI scan, but the visual appearance will
differ from the locked spec.
