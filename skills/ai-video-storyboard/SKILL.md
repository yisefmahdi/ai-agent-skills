---
name: ai-video-storyboard
description: Use this skill whenever the user wants to plan, break down, or generate a storyboard/shot-list for an AI-generated video (Runway, Kling, Luma, Pika, Sora, Midjourney+animation tools, etc.), especially when they mention frame-by-frame breakdowns, "فريمات", 10-second segments, scene breakdowns for AI video, or want to prevent AI hallucination/inconsistency across a long generated video. Trigger this any time the user describes a film/video idea (a story, ad, explainer, music video) and wants it turned into a structured production package - scenes broken into 10-second segments broken into per-second frames, each frame with a full prompt (visual description, camera angle, lighting, motion/transition, dialogue, voice tone, music/SFX), organized as numbered image folders plus a master text prompt file plus an Excel tracking sheet. Also use this any time the user asks to continue, extend, or add scenes to a storyboard project already started with this workflow.
---

# AI Video Storyboard Generator

## What this skill does

Turns a video idea (any length, but designed around a 60-second default) into a **frame-by-frame production package** ready to hand to an AI image/video generation tool (Runway, Kling, Luma, Pika, Midjourney, etc.). The whole point is to eliminate AI hallucination across long generations by breaking everything into small, tightly-specified, individually-generatable units — never asking a generator to imagine more than ~1 second of new content at a time without an explicit anchor.

The output for every project is always three things:
1. A **folder structure** with one numbered folder per 10-second segment, each meant to hold that segment's generated frame images.
2. A **master prompt text file** per segment (or one combined file — see Output Format) containing a complete, literal, nothing-left-to-imagination prompt for every single frame in that segment.
3. An **Excel tracking sheet** (`storyboard.xlsx`) summarizing every scene/segment/frame as a scannable table.

## Core structure (memorize this hierarchy)

```
Video (e.g. 60s)
 └─ Scene (narrative beat, variable length — e.g. "Scene 1: The Crash", 20s)
     └─ Segment (fixed 10-second production chunk)
         └─ Frame (1 image per ~1 second of segment, MORE if the action is fast/complex)
```

- **Scenes** are narrative units — decided by story beats, not by a fixed duration. A calm dialogue scene might be 20s; a fast action beat might be 10s.
- **Segments** are always chunked in **10-second blocks** regardless of scene boundaries. If a scene is 23 seconds, that's 3 segments (10s + 10s + 3s, or rebalance to 3 segments of ~7-8s — ask the user which they prefer if it's not obvious).
- **Frames** default to **1 per second** (so a 10s segment = 10 frames minimum). Increase frame density beyond 1/sec for fast motion, quick cuts, or complex action within a segment — use judgment and say so explicitly in the plan (e.g. "Segment 3 has a helicopter explosion, using 14 frames instead of 10 to capture the debris beat-by-beat"). Never go below 1 frame/second.

## Workflow — follow these steps in order every time

### Step 1: Gather story + technical parameters

If the user already gave you a story/concept in the conversation, don't re-ask for it — extract what you can and confirm gaps. Otherwise ask. You need, at minimum:

- **The story/concept** — even a rough pitch is enough to start; you'll break it into scenes yourself and confirm with the user.
- **Total target duration** (default 60s if unstated — confirm).
- **Aspect ratio** (9:16 vertical, 16:9 horizontal, or 1:1 — always ask if not stated, never assume).
- **Character/location references** — ask if the user has reference images for characters, creatures, or locations they'll supply to the generation tool. If yes, note in the prompt file where each reference should be used (e.g. "Use uploaded reference [Girl_Character.png] for consistency"). If no images yet, still write full text descriptions so the prompt works standalone.
- **Prompt language**: default to **English** for all visual/camera/motion prompts (AI generation tools respond best to English). For dialogue/voice lines, ask whether the user wants them in Arabic, English, or both — never assume.
- **Dialogue/voice**: does this video have spoken lines, narration, or is it visual-only with music/SFX?

Use `ask_user_input_v0` for these if more than one is genuinely unclear — but if the user already answered several of these earlier in the conversation, don't re-ask, just confirm your assumptions briefly and move on.

### Step 2: Break the story into Scenes

Read the story and split it into narrative beats (Scene 1, Scene 2, ...). For each scene, define:
- Scene title (short, e.g. "The Crash")
- Story beat / what happens (1-2 sentences)
- Approximate duration
- Setting/location
- Characters present
- Emotional tone (this drives lighting, color grade, pacing, music choices downstream)

Present this scene breakdown to the user **before** generating the full frame-by-frame prompts, so they can correct the story direction cheaply. This is a natural checkpoint — a short confirmation, not a full elicitation round.

### Step 3: Break each Scene into 10-second Segments

For each scene, divide its duration into 10-second segments (see chunking rule above). Number them globally and sequentially across the whole video, e.g.:
- `Scene 1 / Segment 01` (0:00–0:10)
- `Scene 1 / Segment 02` (0:10–0:20)
- `Scene 2 / Segment 03` (0:20–0:30)
- ...

### Step 4: Build per-Segment Frame Prompts

This is the core deliverable. For **every segment**, write out **every frame** with a complete, literal prompt. Read `references/prompt_template.md` before writing these — it has the exact field structure and a full worked example (the polar-bear-and-girl story) to match tone and specificity against. Every frame prompt must be self-contained enough that a generator with zero memory of prior frames could still produce a consistent result, because that's the whole anti-hallucination mechanism: specificity over reliance on model memory.

Non-negotiable rules for frame prompts:
- **Continuity anchoring**: every frame after the first in a segment must explicitly reference what carries over from the previous frame (character position, expression, lighting direction, camera position) — never let the generator guess what stayed the same.
- **One new change per frame**: each frame should advance the action by roughly one beat/one second's worth of change from the frame before it — not a full new scene each time.
- **No vague language**: never write things like "she looks sad" alone — specify *how*: eyebrows, mouth, gaze direction, body posture, breathing, tears or none, etc. Same for camera: never just "camera moves" — specify pan/tilt/dolly/zoom, direction, speed (e.g. "slow dolly-in, 2 seconds, from medium shot to close-up").
- **Every frame prompt includes ALL of these fields** (full spec + examples in `references/prompt_template.md`):
  1. Frame number + timestamp
  2. Visual description (characters, action, setting, composition)
  3. Camera (shot type, angle, movement)
  4. Lighting (source, color temperature, mood)
  5. Motion/transition into the NEXT frame (how this frame animates or cuts forward)
  6. Dialogue/voice line (exact text, in the language the user requested) — or "none" if silent
  7. Voice tone/delivery direction (e.g. "whispered, trembling, out of breath") — only if there's dialogue
  8. Music/SFX cue for this moment (mood, instrumentation, or specific sound effect)
  9. Aspect ratio (repeat every frame — generators are stateless, don't rely on it being remembered)
  10. Continuity note (what must visually match the previous frame)

### Step 5: Generate the deliverables

Read `references/output_format.md` for the exact folder layout, file naming convention, the Excel column schema, and the xlsx skill usage notes. In short:
- Create the folder tree (one folder per segment, named `Scene##_Segment##_[shortname]`).
- Write one `prompts.txt` inside each segment folder with all that segment's frame prompts, formatted per the template.
- Build `storyboard.xlsx` at the project root summarizing every scene/segment/frame as rows (this is a **spreadsheet deliverable** — consult the `xlsx` skill for how to build it correctly, don't hand-roll it).
- Do NOT generate actual images yourself — Claude cannot generate the frame images. Folders are created empty (or as placeholders) for the user to fill by running each segment's `prompts.txt` through their AI image/video tool.

### Step 6: Present and confirm

Share the folder + files with the user via `present_files`/`Artifact` as appropriate, and briefly point out anything they should double check (e.g. "Segment 5 has 13 frames instead of 10 because of the explosion — let me know if you want it split into two segments instead").

## Extending an existing project

If the user says "add another scene" or "continue the story" for a project already built this way, read back their existing `storyboard.xlsx` and segment folders (if available) to pick up the last used numbering, established character/location descriptions, and tone — then continue the same numbering sequence rather than restarting at Scene 1 / Segment 01.

## Reference files

- `references/prompt_template.md` — exact frame-prompt field structure + a fully worked example segment (polar bear rescue story) to calibrate tone/specificity. **Read this before writing any frame prompts.**
- `references/output_format.md` — folder/file naming conventions, prompts.txt formatting, and the Excel column schema. **Read this before generating deliverables.**