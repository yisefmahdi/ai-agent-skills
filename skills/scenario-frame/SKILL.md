---
name: scenario-frame
description: Use this skill whenever the user wants to turn an ad/video script (سيناريو) into a frame-accurate production storyboard delivered as a single Excel file. Especially trigger when they mention "استدعاء الاسكيل", "Scenario-Frame", generating keyframe prompts + motion/animation prompts per shot, variable shot durations (e.g. "4 أو 6 أو 10 ثواني"), a negative prompt row, or a references/characters table with Pinterest search lines. This skill auto-splits raw dialogue into scenes and shots by sentence/idea boundaries, computes each shot's duration from its actual word count (not guesswork), decides how many keyframe images each shot needs based on motion complexity, grounds character/product/location descriptions in any uploaded reference images rather than guessing from text alone, and proactively asks the user about any contradiction or ambiguity in the script (or between the script and uploaded images) BEFORE building the Excel file. Trigger on continuing/extending a project already built with this workflow too.
---

# Scenario-Frame — من السيناريو للفريمات بدقة إنتاجية

**Scenario-Frame** يحوّل سيناريو خام (أي لغة) لحزمة إنتاج جاهزة: فريمات دقيقة، تحليل حركي فيزيائي، مرجعيات ثابتة، وحماية صريحة من هلوسة الذكاء الاصطناعي — كل هذا بملف إكسل واحد.

## What this skill does

Takes a raw ad/video script (any language) plus two settings — **aspect ratio** and **the allowed shot-duration range** (e.g. 4 / 6 / 10 seconds) — and produces **one Excel file** containing:
1. A **main table**: one row per shot, with a flexible number of keyframe-image prompt columns (as many as that shot's motion actually needs), a full physical-motion prompt, dialogue, visual summary, and status.
2. A **fixed Negative Prompt row** at the bottom — written specifically to block the exact hallucination failure modes this skill is designed to prevent (see "Negative prompt is a second line of defense" below).
3. A **References table** (characters / locations / products / outfits), placed under the main table in the same sheet — one block per entity, each with a full locked visual description **and a ready-to-paste Pinterest search line** for finding real visual references.

The whole point is **zero hallucination across independently-generated frames and shots** — every design decision below exists to close one specific hallucination failure mode.

## Required inputs before building anything

Only three things are truly required. If the user already gave all three in one message, don't ask — just confirm briefly and proceed. If any is missing, ask for it (use `ask_user_input_v0` if more than one is missing).

1. **The script itself** (السيناريو) — raw dialogue/narration text, any length.
2. **Aspect ratio** — 9:16 / 16:9 / 1:1 / other. Support whatever the user states; ask if not given.
3. **Allowed shot-duration range** — the exact set of durations the target AI video-generation tool actually supports (e.g. "4, 6, 10 ثانية"). This is **not a preference Claude proposes** — different generation tools have hard, different duration limits, so this must come from the user, who knows which tool/model they're generating with. **Always ask for this explicitly if not given** — never assume a default range or invent one, since snapping to a range the user's actual tool doesn't support makes the whole sheet unusable. If the user gives an open/free range ("أي رقم مناسب", no tool constraint), skip snapping (Step 3's snapping sub-step below) and use the raw computed duration directly.

Everything else (character/product/location reference **images**, voice casting notes, music direction, specific camera brand/lens language, etc.) is optional and only improves the output if supplied — never block on it. But if the user uploads reference images, Step 1.5 below is mandatory before writing any prompt.

## Step 1.5 — If the user uploaded reference images, actually look at them first

If one or more reference images are attached (a character, a product, a location, an outfit — anything), **view each one with the `view` tool before writing a single prompt**. Never write a visual description from the script's text alone when a reference image for that entity exists — the image is ground truth and the script's wording is not a substitute for it.

For each reference image:
- Extract the concrete visual facts the script could never specify on its own: exact color (not "blue" — the actual shade), material/texture, precise proportions, logo/label placement and exact text if a product, distinguishing marks, exact garment cut, background details if it's a location photo.
- These extracted facts become the **locked description** for that entity in the References table (Step 7) — written from what you actually saw in the image, not inferred or guessed.
- If the script's text description of that entity conflicts with what the reference image actually shows (e.g. script says "white mug," image shows a green one), **flag this to the user as part of Step 1's ambiguity/contradiction check** rather than silently picking one — the image usually wins for visual fact, but confirm rather than assume.
- If multiple reference images are given for the same entity (e.g. two angles of a character, or packaging front/back of a product), note what each one shows and use whichever is relevant per shot (e.g. a side-angle shot should pull from a side-angle reference if one exists).

Every downstream frame prompt referencing that tag should reflect what was actually seen in the image — this is the single biggest accuracy upgrade available when references exist, so treat this step as mandatory, not optional polish.

## Step 1 — Validate the script BEFORE building anything (mandatory gate)

Before splitting into scenes/shots or writing a single prompt, read the full script closely (and, if reference images were uploaded, view them too — see Step 1.5 — since a script/image mismatch is itself a contradiction to flag here) and actively look for:

- **Contradictions**: e.g. a prop described in one line that disappears or changes in another without explanation; a physical action that's physically impossible in sequence (e.g. character described as sitting, then the very next line says they're "standing up" with no transition described).
- **Ambiguity that would force Claude to invent facts**: e.g. an action is named but not *how* (a hand gesture pointed at what, exactly?); a line implies a prop or costume change with no description of what it changes to; a scene's setting is never stated.
- **Mismatched pacing signals**: e.g. a very short line of dialogue paired with a stage direction describing a long, complex physical action that could not fit the line's natural speaking duration — or the reverse (a long line with "no movement" when the ad clearly needs visual interest).
- **Missing continuity anchors**: nothing to indicate how one shot's ending pose relates to the next shot's starting pose (fine if it's an intentional hard cut — but check this is intentional, not an oversight).

If you find any of these, **stop and ask the user specific, concrete questions about exactly what you found** — never silently assume or paper over a gap. Don't ask generically ("is there anything unclear?") — name the exact line and the exact gap. Use `ask_user_input_v0` when there are multiple concrete gaps to resolve. Only proceed to Step 2 once resolved (or the user explicitly says to proceed with your best assumption, which you then state plainly in the sheet).

## Step 2 — Auto-split the script into Scenes and Shots

Do this from the raw dialogue itself — the user does not pre-mark scene/shot boundaries.

- **A large narrative beat / topic shift** → new **Scene**.
- **Each sentence or self-contained idea within a scene** → a candidate **Shot**.
- **If a single shot's stage direction implies multiple distinct camera angles** (e.g. a wide establishing moment followed by a close reaction within what was written as one beat), **split it into multiple shots** — one per angle — rather than cramming multiple camera setups into one shot's duration.

## Step 3 — Compute each shot's duration: word count AND visual complexity together

This is the single most important correction in this skill: **duration is not a pure word-count formula.** Word count tells you the *minimum* time the dialogue needs to not sound rushed. Visual/camera complexity tells you whether the shot has enough happening on screen to justify sitting in it longer than that minimum. A shot needs **both** signals before picking a final duration — never duration from word count alone, and never duration from "this idea sounds big" alone (the mistake made earlier in this project).

**Sub-step A — compute the dialogue-minimum:**
```
raw_seconds = word_count(shot's dialogue) / speaking_rate
dialogue_minimum = raw_seconds + padding
```
- **speaking_rate**: default **~2.3–2.5 words/second** for calm, confident-register spoken ad delivery (adjust down toward ~2.0 for a slow/solemn register, up toward ~2.8–3.0 for an energetic/fast register — infer the right register from the script's tone, or ask if genuinely unclear). State the rate you used once, visibly, in the Overview area.
- **padding**: add **~0.8–1.2 seconds** total (a short beat before the first word, a short beat after the last word so the shot doesn't feel clipped).
- **Silent/visual-only shots** (no dialogue): skip Sub-step A — base duration on Sub-step B alone (the described action's natural physical duration).

**Sub-step B — read the shot's visual/camera complexity:**
Ask: does this shot have more happening visually than the dialogue-minimum alone would show? Signals that push duration *up* beyond the dialogue-minimum:
- More than one camera angle or setup within the shot (per Step 2, this usually means it should already be split into multiple shots — but if the user wants it kept as one continuous take, it needs more time)
- More than one distinct physical beat/gesture (not just one continuous motion)
- A location or framing change within the shot

Signals that mean the shot should sit at the **lowest value in the user's range that still fits the dialogue-minimum** — don't pad it longer just because the range offers a bigger option:
- Single static camera setup, one location, no framing change
- One continuous, simple gesture or no gesture at all
- Nothing new enters the frame after the first second

**Sub-step C — pick the final duration:**
- If the shot is visually simple (second bullet list above) and the user's range has a value that comfortably fits `dialogue_minimum`, use **that smallest sufficient value** — don't jump to a larger range option just because it exists. A simple single-camera shot sitting in a long duration with nothing new to look at is its own kind of flaw (dead air), not a safe default.
- If the shot has real visual/camera complexity (first bullet list above) and `dialogue_minimum` falls in a gap between two range values, lean toward the **larger** one — the extra time is justified by actual on-screen content, not wasted.
- If `dialogue_minimum` falls in a gap between two range values and the shot is visually simple, still don't round down below `dialogue_minimum` (never rush/clip dialogue) — but actively consider whether the shot's visual content can be enriched (an added small gesture, a secondary detail) to justify the longer duration you're forced into by the range, and say so explicitly, rather than silently padding with dead air.
- If the user's range genuinely has no value that fits without either rushing dialogue or padding dead air, say so plainly — this is a real constraint to surface, not to silently paper over.

**Show your work**: for every shot, make both the word-count arithmetic and the visual-complexity reasoning checkable in the sheet (or your reply) — not just the final duration, so the user can verify the reasoning rather than receive a black-box number.

## Step 4 — Decide how many keyframe images each shot needs

Never hardcode "always 2" or "always N." Decide per shot from two factors:

1. **Duration**: minimum image count ≈ `ceil(shot_duration / 4) + 1`. A shot ≤5s needs 2 (start/end). A shot around 6-8s typically needs 3 (start/mid/end). A shot ≥9-10s typically needs 4, spaced roughly every 3-4 seconds — because **no gap between two consecutive keyframes should exceed ~3-4 seconds of undescribed motion**, or the generation tool starts inventing the in-between action (this is the Motion Gap hallucination).
2. **Motion complexity**: if a shot contains more than one distinct physical beat (e.g. "points at self, then points at the room" — two separate gestures), add an image at the transition point between beats even if duration alone wouldn't require it. A shot with a single continuous smooth motion needs fewer images than a shot of the same length with multiple discrete beats or a repeating/cyclical motion (like a repeated head-shake or finger-wag) — repeating motions need enough images to document more than one cycle, or the tool will guess how many repetitions happened.

State briefly, per shot, why that image count was chosen (one short clause is enough) — this keeps the decision auditable instead of arbitrary.

## Step 5 — Write the frame prompts (keyframe images)

Each keyframe image prompt must be **fully self-contained** — a generator with zero memory of other frames must be able to produce a consistent result from this prompt alone.

Required in every image prompt:
- Frame label + timestamp within the shot (e.g. "فريم 2 — 0:03.3")
- Full visual description: character pose, expression, props, setting — reusing the **exact locked wording** from that entity's References table entry (see Step 7) rather than re-describing from memory each time, to prevent Identity Drift.
- Camera: shot type, angle, movement state (static/panning/etc.) — repeated every time, never assumed carried over, to prevent Camera Drift.
- Aspect ratio — repeated every time, to prevent Aspect Ratio Drift.

**Continuity Bridge (mandatory, solves Cross-Shot Continuity hallucination):** the first image prompt of every shot (after the first shot) must open with one explicit clause stating the exact pose/expression/camera state it is continuing from — taken verbatim from the previous shot's final image description. If the cut is an intentional hard cut (different pose is fine), say so explicitly ("قطع متعمد — ما في استمرارية مقصودة هون") rather than leaving it ambiguous, so it's clear the mismatch was a choice, not an oversight.

## Step 6 — Write the motion/animation prompt (physical realism, mandatory depth)

This is the "تحليل حركي فيزيائي بدقة عالية" the user asked for — never write vague motion language. For every shot's motion prompt, apply all of these:

- **Timestamp every distinct beat** within the shot, down to fractions of a second where it matters (e.g. "0:01.8" not just "then").
- **Joint sequencing**: a limb's motion should describe which joint leads and which follows, with a realistic lag (~80-150ms is a reasonable default to describe, adjust to the gesture) — shoulder leads, elbow follows, fingers follow last, etc. Never let two joints "snap" into position simultaneously unless the action genuinely is instantaneous (e.g. an eye blink).
- **Ease-in/ease-out, never linear**: motion accelerates away from a resting position and decelerates into a new one. Oscillating/repeating motions (headshake, finger-wag) behave like a damped pendulum — describe the deceleration pattern, not constant-speed looping.
- **Overlap between consecutive beats** where natural (e.g. one arm beginning to lower while the other begins to rise) rather than every beat starting only once the previous one fully completes — real bodies move this way.
- **State what stays constant** (camera, lighting, background elements) as explicitly as what changes — omissions here are exactly what the Negative Prompt (Step 8) exists to guard against, but the positive prompt should still say it.

## Step 7 — Build the References table (characters / locations / products / outfits)

Placed in the **same sheet**, **below** the main shot table and the negative-prompt row. One block per distinct entity referenced anywhere in the script (character, location, product, a costume/outfit if it changes mid-script, a key prop if it recurs and matters for consistency).

Columns:
| Column | Content |
|---|---|
| الرمز (Tag) | e.g. `@شخصية-1`, `@موقع-2`, `@منتج-1` |
| النوع | شخصية / مكان / منتج / ملابس / غرض متكرر |
| الاسم | As named in the script, or a short descriptive label if unnamed |
| مصدر الوصف | "من صورة مرفوعة" or "من وصف النص" — states plainly whether this entity's locked description came from an actual uploaded reference image (Step 1.5) or was written from the script's text alone, so the user knows which entities are image-grounded and which are text-inferred |
| الوصف الكامل الثابت | The full, locked, literal visual description — this is the exact text every frame prompt referencing this tag should reuse verbatim for its core description, not paraphrase differently each time. When sourced from an image, this should reflect what was actually seen (Step 1.5), not generic/assumed detail. |
| جملة بحث Pinterest | A ready-to-paste search line for finding real visual references matching this entity's style, in the **same language as the original script**. Still useful even when a reference image exists (e.g. to find more angles/poses), so always include it. |

This table is the single source of truth for every recurring entity — frame prompts should reference the tag and restate its locked description rather than re-inventing wording per frame (this is what actually prevents Identity Drift at scale, not just saying "same character").

## Step 8 — Negative prompt is a second line of defense, not decoration

Write **one fixed negative-prompt block** at the bottom of the main table (its own labeled row), meant to be pasted alongside every image/video generation call for the whole project. It must explicitly counter **every hallucination category this skill targets** — don't write a generic negative prompt; write one with a clause for each of:

- Identity drift (character design/outfit/face changing from the locked References description)
- Setting drift (background props moving, disappearing, or changing from the locked description)
- Camera drift (unrequested shot-type or angle change)
- Aspect ratio drift
- Physics violations (sudden/linear/non-eased motion, joints snapping together, impossible limb positions)
- Extra/missing/malformed fingers and facial distortions
- Unwanted text, logos, or watermarks burned into the image
- Lighting/color inconsistency across frames
- Style drift away from the specified art style

Write it in the **same language as the original script**, same as every other prompt field.

## Step 9 — Validation row before delivering

Before saving, add one small checkable summary (can live in an Overview area or as a final row):
- Sum of all shot durations = stated total ad length? (If not, say so — don't silently adjust one to force a match.)
- Every shot's image count matches the Step 4 rule given its final (snapped) duration?
- Every shot after the first has a Continuity Bridge clause (or an explicit "intentional cut" note)?

If any check fails, fix it before presenting the file — don't deliver a file you haven't self-checked.

## Step 10 — Build and deliver

Read the `xlsx` skill (`/mnt/skills/public/xlsx/SKILL.md`) before writing the file — don't hand-roll spreadsheet XML, and run `recalc.py` before delivering even though this workbook has no formulas (it confirms the file opens cleanly). See `references/sheet_layout.md` for the exact column set, row order, and formatting conventions (including a hard rule: never italicize wrapped Arabic data cells — it can render as broken fragments instead of clean lines).

Before presenting the file, render a quick visual preview (e.g. `soffice --headless --convert-to png`) and actually look at it — especially any column carrying dense wrapped text — rather than trusting that wrap_text=True alone guarantees clean rendering. This is cheap insurance against delivering a visibly broken cell to the user.

Save to `/mnt/user-data/outputs/`, then `present_files`.

## Extending an existing project

If the user asks to add scenes/shots to a project already built this way, read back the existing sheet (References table included) first — reuse established tags, locked descriptions, and the same speaking-rate assumption — rather than restarting numbering or re-describing entities from scratch.

## Reference files

- `references/sheet_layout.md` — exact column order for the main table, negative-prompt row formatting, and the References table layout. Read before writing the Excel file.
