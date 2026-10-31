# Sheet Layout — Main Table, Negative Prompt Row, References Table

Everything lives in **one sheet** (plus an optional short "Overview" sheet if the project has many scenes — same convention as before). Order, top to bottom, within the main sheet:

1. Main shot table (header row, frozen)
2. Total duration row
3. Negative prompt row (fixed, one block, spans all columns)
4. A one-line usage note under the negative prompt
5. References table (characters/locations/products/outfits), a few rows below

## 1. Main table columns, in order

| Column | Content |
|---|---|
| اللقطة | Shot number + short label, e.g. "3 (المهارات)" |
| المدة | Final snapped duration, e.g. "6 ث" |
| عدد الكلمات → المدة المحسوبة | Short audit string, e.g. "12 كلمة ÷ 2.4 = 5.8 ث" — makes Step 3's arithmetic checkable at a glance |
| برومبت الصورة 1 … N | As many image-prompt columns as the **widest shot in this project** needs (computed per Step 4). Narrower shots simply leave the extra cells blank (light-gray fill) rather than every shot being forced to the max column count's worth of content. |
| شو بتشوف (الوصف) | Short one-line human-readable summary of the shot, same language as the script |
| الصوت / الحوار | Exact dialogue line, or "بدون حوار" |
| برومبت التحريك | The full physical-motion analysis from Step 6 |
| حالة اللقطة | Status, left blank/default "جاهز" unless the user says otherwise |

Keep the same RTL/LTR, font (Arial), border, freeze-pane, and alternating scene-fill conventions used in prior builds of this project unless the user says otherwise.

## 2. Total duration row

One row: label cell + merged total-seconds cell across the rest. Bold.

## 3. Negative prompt row

One visually distinct row (e.g. dark red header cell labeled "البرومبت السلبي (ثابت)", merged light-red body cell with the full negative prompt text per Step 8). Give it enough row height to read comfortably — this text is dense by design.

## 4. Usage note

One small italic line under the negative prompt row, same language as the script, reminding the user this block gets pasted with every single generation call for the project (not re-written per shot).

## 5. References table

A few blank rows below the negative prompt note, then:

| الرمز | النوع | الاسم | الوصف الكامل الثابت | جملة بحث Pinterest |
|---|---|---|---|---|
| @شخصية-1 | شخصية | (as named in script) | full locked description | Pinterest search line, same language as script |
| @موقع-1 | مكان | ... | ... | ... |
| @منتج-1 | منتج | ... | ... | ... |

One row per distinct entity. This is the **single source of truth** — image prompts in the main table should quote this table's locked description verbatim for that tag rather than re-describing the entity differently each time.

## Column widths / row heights (practical defaults)

- Image-prompt columns: ~32-36 width (they carry the densest single-image text)
- Motion-prompt column: ~46-50 width (carries the densest text in the whole sheet)
- Dialogue / visual-summary columns: ~28-32 width
- Shot / duration / status columns: narrow, ~10-14 width, centered
- Data rows: tall enough for wrapped dense text — 170-200 height is a reasonable starting point, adjust per actual content length
- References table rows: ~50-70 height (locked descriptions are long; Pinterest lines are short)

## Formatting reminders (apply exactly as in prior builds)

- Arial font throughout
- **Never use italic for any Arabic data-cell text, especially in narrow wrapped columns.** Long wrapped Arabic text in italic can render as broken/garbled line fragments in some renderers (observed in the audit column of an earlier build) instead of clean wrapped lines. Use regular (non-italic) weight for every data cell; reserve italic only for very short, non-wrapping single-line notes (e.g. a one-line usage reminder that fits on one line without wrapping).
- RTL sheet view when the script is Arabic (`ws.sheet_view.rightToLeft = True`)
- Header row: dark blue fill, white bold text, centered, frozen
- Alternating light-blue/white fill per shot row for scannability
- Unused image-prompt cells (shots needing fewer images than the project max): light-gray fill, left blank — not "N/A" text, just visually muted
- Negative prompt row: distinct dark-red header + light-red body fill so it reads as a different kind of row, not just another data row
- Run `recalc.py` from the xlsx skill before delivering, even though this workbook carries no formulas — it's the cheapest possible proof the file opens cleanly
- **Before delivering, render a quick visual preview** (convert the sheet to an image, e.g. via `soffice --headless --convert-to png`) and actually look at it, especially any column carrying dense wrapped Arabic text — catching a rendering glitch (like the italic issue above) before the user sees it is cheap; catching it after is not
