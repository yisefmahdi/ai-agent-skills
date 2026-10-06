---
name: ai-video-storyboard
description: Plan and create AI film assets, including screenplays, shot lists, storyboards, character and location reference sheets, posters, video prompts, ultra-detailed image-to-prompt reverse engineering, and frame-by-frame reel analysis for AI video reproduction. Use when the user asks to develop or prepare visual materials for AI-generated film, convert an image into a high-fidelity generation prompt, or analyze a video reel for strategic or AI reproduction purposes; identify the requested deliverable, preserve supplied story and reference details, and follow the user's language and duration constraints.
---

# AI Video Storyboard, Screenplay & Hollywood Studio Director Master Engine (v8.0)

## Overview

The `ai-video-storyboard` skill is a complete, studio-grade Hollywood virtual production and directing pipeline engineered specifically for AI filmmaking, luxury commercial advertising, viral short-form social video, **ultra-detailed image-to-prompt reverse engineering**, and **frame-by-frame reel analysis for AI video reproduction and strategic analysis**.

In **v8.0**, the system supports distinct production deliverables and helps reduce common continuity, framing, motion, and prompting errors. AI image and video models remain stochastic; these procedures improve clarity but cannot guarantee exact rendering, legible image text, or acceptance by a model's safety filters.

> **v8.0 changes:** Two major new modes: **IMAGE-TO-PROMPT** (reverse-engineer any image into an ultra-detailed AI generation prompt with exact dimensions, style, lighting, composition, and edit/swap instructions) and **REEL ANALYSIS** (decompose video reels at ~3 frames/second with cut detection, segment mapping, and AI-ready reproduction prompts with persistent output files). All previous v7.0 features remain: project-agnostic templates; image roles labeled explicitly; `prompts.txt` and folder trees created only for a requested production package; new `scripts/analyze_reel.py` extracts frames and generates structured analysis templates.

## Quick Deliverable Router

When this skill is invoked, infer the requested output from the user's request and work only on that deliverable. The user may invoke the skill first and then ask naturally; they do not need to complete a form. If the interface supports slash commands, the user may start with `/ai-video-storyboard` and then name a mode. Otherwise, select or mention `ai-video-storyboard` in the usual way.

Supported modes:

- **SCREENPLAY / SHOT PLAN** — write or revise the script, preserve source facts, and add time-coded dramatic beats or camera coverage when requested.
- **STORYBOARD** — create an English image-generation prompt or inspect a generated board. Distinguish a storyboard for one generation unit from a longer sequence board.
- **CHARACTER BIBLE** — create one identity-locked profile/reference sheet per character, with facts separated from proposed design choices.
- **LOCATION / SET BIBLE** — define the approved layout, entrances, geography, lighting, and continuity of a location.
- **FILM POSTER / THUMBNAIL** — create key art and optional title/tagline layout. Do not force a storyboard or video prompt into this mode.
- **VIDEO PROMPT** — create the final video prompt after reviewing the approved storyboard and its reference roles, unless the user explicitly requests another workflow or already supplies an approved board.
- **IMAGE-TO-PROMPT** — reverse-engineer any supplied image into an ultra-detailed AI image-generation prompt. Supports element swapping (replace a person, text, object, or background) while preserving all other visual properties. Always output the prompt to screen and optionally save to a file in the active project directory.
- **REEL ANALYSIS** — decompose a video reel frame-by-frame (~3 captures per second) with scene-cut detection, segment mapping, and comprehensive visual/cinematic analysis. Always saves output files (`reel_analysis.md` and `reel_prompts.txt`) for reuse.
- **PRODUCTION PACKAGE** — combine only the modes the user asks for, in the requested order.

Default response language follows the user. Write production prompts and on-image copy in the language the user specifies; when they request English, deliver the prompt and exact image text in English. State which supplied image is the identity reference, location reference, layout/style reference, or start/bridge frame. Do not treat one reference role as another.

### Scene Duration vs. Generation Duration

A dramatic scene may be longer than 10 seconds. A generated video file must obey the user's and target tool's maximum duration; use **10 seconds as the default maximum** for this workflow, and never exceed a stricter limit the user has set. Break longer scenes into generation units at logical dramatic beats. Record each unit's time range, action, camera move, end state, and the next unit's matching start state. A storyboard may cover a longer scene as an editorial shot plan, but it must map every shot to generation units and must not imply one long video generation.

---

## The Seventeen Master Production Pillars

### 1. The Storyboard-First & Sheet-Driven Video Protocol
Use storyboard-first ordering for a video-generation workflow: prepare and inspect the relevant board before writing the final video prompt. This ordering does not apply to standalone posters, character sheets, location sheets, or screenplay edits.

- **Generation-unit board:** For one video unit up to 10 seconds, use the 16:9 4×3 layout (10 chronological stills plus the audio and director-audit cards), or the applicable vertical layout. Mark the exact unit time range and its start/end continuity states.
- **Sequence/scene board:** A board may cover a longer dramatic scene and may contain a custom number of editorial shots. Label it as a shot plan, state each shot's screen time, and map shots to separate generation units. Never imply the whole scene is one generation.
- **Audit and video prompt:** Inspect the generated visuals against the script and reference-image roles. Compose the final video prompt afterward, binding it to the approved visuals and the appropriate start/bridge frame.
- **Zero-grid rule applies to video output only:** The generated video starts as full-screen live action. Do not show the storyboard sheet, grid, borders, or captions in the video. This rule does not prohibit panel borders or labels on the storyboard image itself.

---

### 2. Hollywood Optical & Lens Engine (ARRI / Panavision Cinematography)
Replaces vague aesthetics with exact physical cinematography standards, focal lengths, aperture mechanics, depth of field, and color science:
- **Master Establishing Shot (24mm Anamorphic T2.0)**: Expansive vistas, straight rectilinear horizon, natural subtle anamorphic edge barrel distortion, infinite deep depth of field.
- **Narrative Medium & Two-Shot (35mm – 50mm Anamorphic T2.8)**: True human eye perspective (45°–60° FOV) for authentic character interaction and environmental grounding without facial distortion.
- **Emotional Close-Up (85mm T1.4 Shallow DOF)**: Isolates faces with optical background compression, creamy bokeh, razor-sharp iris focus, and visible pores, eyelashes, and atmospheric frost.
- **Tactile Macro Insert (100mm Macro 1:1 T2.8)**: Micro-texture clarity for tactile actions: gloved fingers gripping coarse fur fibers, zipper teeth interlocking, fluid droplets, luxury product packaging details.
- **Kelvin Color Science & Volumetric Lighting (examples — pick per approved look)**:
  - Example palettes: `7500K–8500K cold steel-blue twilight`, `3200K warm tungsten firelight`, `5600K clean balanced daylight`, `10000K luminous sapphire-blue glow`.
  - True volumetric physics: Atmospheric Tyndall scattering, particulate backlighting, subsurface scattering on approved skin/materials.

---

### 3. Anti-Hallucination & Zero-Spin Engine (The Dual-Mode Camera Director)
Solves the primary failure mode where models spin characters 180° like a turntable when reconciling multi-angle descriptions. The director selects ONE explicit mode per shot:
- **Mode A: The Continuous Plan-Séquence / Steadicam Unidirectional Take**:
  Used when generating a single, unbroken camera take from a bridge frame anchor.
  - Camera follows or tracks alongside characters on a fixed linear vector.
  - Characters walk in **ONE continuous forward direction**.
  - `STRICT ANTI-SPIN MANDATE: Characters WALK CONTINUOUSLY FORWARD AWAY FROM (or TOWARD) THE CAMERA throughout all 10 seconds. ZERO 180-DEGREE SPINS, ZERO TURNTABLE TURNING, ZERO REVERSE-ANGLE FLIPS. Maintain unbroken camera perspective throughout.`
- **Mode B: Hollywood Cinematic Coverage & Cut Syntax**:
  Used when commanding the video model to execute multi-panel storyboard edits. Uses formal editing cut syntax to force the diffusion model to cut camera angles rather than rotate 3D bodies:
  - `[CUT TO: LOW-ANGLE INSERT (Panel 3)]`
  - `[MATCH-CUT TO: MEDIUM CLOSE-UP (Panel 6)]`
  - `[CUT TO: MACRO INSERT (Panel 8)]`
  - `[DISSOLVE TO: WIDE MASTER (Panel 10)]`
- **Adult Facial Identity Lock (Anti-De-Aging Protocol)**:
  Use only when the approved reference is an adult and the model regresses age in wide shots. Take age, sex, and bone structure from the user's source — never assume them:
  `[CHARACTER NAME] MATURE ADULT BONE STRUCTURE (ANTI-DE-AGING PROTOCOL): [Character] is strictly a [age]-year-old mature adult [female/male] with [approved face shape, cheekbones, jawline, proportions from the identity reference]. STRICT NEGATIVE: ABSOLUTELY NOT A CHILD, NOT A TODDLER, NOT A BABY, ZERO BABY FACE, ZERO CHILDLIKE PROPORTIONS.`

---

### 4. Biomechanical Micro-Action Staging Engine (Anti-Inertia & Anti-"Just Walking")
For movement-heavy scenes, divide a generation unit into physical milestones that follow the script: initiation, movement or interaction, reaction/consequence, and end state. Use 2-second beats only when useful; do not force walking, contact, weather, a companion, or a destination reveal into a scene that does not contain them. For quiet scenes, articulate the planned change through camera, light, focus, sound, or a restrained character reaction rather than inventing action.

---

### 5. Safety-Aware Pre-Flight Review
This review can make fictional action clearer and less graphic, but cannot guarantee acceptance by a model or platform. Follow the target platform's current rules and preserve the user's intended story:
- **Production framing**: Use fictional-production or staged-action language only when it fits the user's scene and helps describe production context. Do not turn every project into a family film or remove peril from the story without cause.
- **Language choices**: Prefer precise, non-graphic description when compatible with the requested work. Do not apply a fixed substitution dictionary when it would change the plot, character intent, or tone. Do not claim that wording bypasses a safety policy.

---

### 6. Visual-to-Kinematic Binding & Spatial Geometry Audit
When a start/bridge frame is supplied and the shot contains contact, a handoff, or a prop interaction, record the relevant pose, screen position, target, reachability, and before/after prop state. Use only details visible or established by the source. Do not force a hand-coordinate audit on posters, profile boards, landscapes, or shots without interaction.

---

### 7. Contact Geometry & Camera-Axis Continuity
For contact actions, describe the actual surface, direction, and order clearly; use planar contact language when it matches the intended action. Preserve screen direction and the 180-degree axis for continuous coverage where needed. Do not ban natural body turns, camera orbits, or screen-position changes when the script calls for them; motivate and stage them explicitly.

---

### 8. Prop Transfer & Anti-Duplication Mechanics
When a prop is picked up, transferred, used, or set down, state who holds it and when the hand becomes empty. Skip this audit for scenes without prop interaction.

---

### 9. 4-Step Mechanical Causality (When Applicable)
For an action that extracts or stows an item, describe the needed causal steps (reach, open, grasp, remove or reverse) and preserve the item/hand state. Do not force this sequence onto unrelated actions.

---

### 10. Multi-Domain Production Pipelines (Films, Commercials, Viral Reels)
The engine executes 3 distinct specialized production modes:
1. **Cinematic Feature Films & Episodic Series (16:9)**:
   - Deep narrative arcs, bridge frame continuity across 10-second segments, master wide-to-tight coverage.
2. **High-End Commercials & Product Ads (16:9 or 9:16) — The AIDA Engine**:
   - **Attention (0–3s)**: High-speed macro sensory hook, dramatic lighting, hero product reveal.
   - **Interest (3–8s)**: Problem-solving kinetic interaction, tactile engagement, fluid/particle dynamics.
   - **Desire (8–20s)**: Aspirational lifestyle payoff, emotional transformation, premium lighting.
   - **Action (20–30s)**: Pristine hero packshot, elegant typography logo slate, compelling call-to-action.
3. **Viral Short-Form Reels & TikTok (9:16)**:
   - 3-second thumb-stopping visual hook, high kinetic energy, and seamless infinite loop anchor.

---

### 11. Aspect-Ratio-Aware Storyboard Grids
- **16:9 Widescreen Mode**: 4-Column × 3-Row Grid (12 panels: Panels ① to ⑩ movie stills + Panels ⑪ `AUDIO DNA PROFILE` & ⑫ `DIRECTOR LOGIC AUDIT`).
- **9:16 Vertical Mode**: Two Vertical 5+5 Storyboard Sheets (Sheet 1: Panels ①–⑤; Sheet 2: Panels ⑥–⑩).
- For a first generation with no prior clip, do not demand a bridge-frame match in Panel 1. Use the exact bridge frame only when a preceding segment exists and the user supplies or identifies it. For a longer sequence board, use a suitable panel count, label it as an editorial plan, and map every shot to its generation unit.

---

### 12. The Master Screenplay & Scriptwriting Engine
- Industry-standard screenplay formats (`INT./EXT.`, action blocks, character dialogue, subtext, auto-segmentation into 10s units).

---

### 13. The Unified Single-File Contract (`prompts.txt`)
When the user requests a complete segment package, use one comprehensive text file named `prompts.txt` with the relevant sections below. Do not create this package for a request that only asks for one poster, one character sheet, or one prompt.
1. `[NARRATIVE REALITY & CHARACTER DNA LOCK]`
2. `[SPATIAL GEOMETRY & ANCHOR AUDIT]`
3. `PART 1: MASTER STORYBOARD SHEET PROMPT`
4. `PART 2: INSTANT STORYBOARD-TO-VIDEO ENGINE PROMPT`
5. `PART 3: SEQUENTIAL SECOND-BY-SECOND BREAKDOWN`
6. `PART 4: DIRECTOR'S LOGICAL & PHYSICAL SANITY AUDIT`

---

### 14. Dual Bridge Frame Protocol
- Continuous episodic matching using `scripts/extract_bridge_frame.py --video <path> --out <path>` (video mode) or `--sheet <path> --panel 10 --format 16x9 --out <path>` (sheet-crop fallback) to extract the exact terminal frame/state. Record the source timecode when the unit is shorter than the maximum.

---

### 15. Cinematic Marketing & Studio Distribution Module
- Professional 16:9 YouTube Thumbnails with 3D frosted typography.
- 9:16 Vertical Theatrical Posters with studio billing blocks.
- Bilingual press releases and viral social media captions.

---

### 16. IMAGE-TO-PROMPT — Ultra-Detailed Image Reverse Engineering Engine (v8.0)

Converts any supplied image into an exhaustive, production-grade AI image-generation prompt. The engine analyzes and captures **every** reproducible visual property of the source image.

#### When to use
- The user uploads an image and asks for a prompt to reproduce it, modify it, or use it as a base.
- The user wants to swap, replace, or edit a specific element (person, text, object, background) while keeping everything else identical.
- The user needs a detailed reference prompt for style transfer, composition matching, or visual consistency.

#### Analysis dimensions (all mandatory in the output prompt)

1. **Exact Dimensions & Aspect Ratio**: Detect and state the pixel dimensions (e.g., 1920×1080), aspect ratio (16:9, 9:16, 1:1, 4:5, etc.), and orientation (landscape/portrait/square).
2. **Visual Medium & Rendering Style**: Photorealistic photography, digital illustration, 3D render, anime, oil painting, watercolor, vector, cinematic still, etc. Include sub-style (e.g., hyper-realistic CGI, editorial fashion photography, Pixar-style 3D).
3. **Camera & Lens Properties** (for photographic images): Estimated focal length, depth of field, aperture/bokeh quality, lens distortion, motion blur, film grain, sensor noise.
4. **Composition & Framing**: Rule of thirds, centered, symmetrical, golden ratio, leading lines, negative space placement, subject position in frame (quadrant), horizon line position.
5. **Lighting Analysis**: Direction (front, side, back, rim, top, bottom), quality (hard/soft/diffused), number of light sources, color temperature (Kelvin estimate), shadows (hard/soft/ambient), specular highlights, volumetric effects, lens flare.
6. **Color Palette & Grading**: Dominant colors (hex codes when possible), color harmony (complementary, analogous, triadic), saturation level, contrast level, tonal range (high-key/low-key/mid-tone), color grading style (teal-orange, desaturated, vivid, matte, film emulation).
7. **Subject Description**: Exhaustive physical description of every subject — people (age, gender, ethnicity, facial features, expression, body pose, gaze direction, hair, skin texture), objects, animals, text content, logos.
8. **Wardrobe & Styling** (for people): Every garment, accessory, material, texture, color, pattern, fit, brand-agnostic description, jewelry, makeup, hairstyle.
9. **Environment & Background**: Setting type (indoor/outdoor/studio), location details, architecture, vegetation, sky condition, floor/surface, depth layers (foreground, midground, background), environmental effects (fog, rain, dust, smoke).
10. **Text & Typography** (if present): Exact text content, font style (serif/sans-serif/script/display), weight, size relative to frame, color, position, effects (shadow, outline, glow, 3D), language.
11. **Mood & Atmosphere**: Emotional tone, energy level, narrative implication, cinematic genre feel.
12. **Post-Processing & Effects**: Vignette, blur, grain, chromatic aberration, glow, double exposure, glitch, overlay textures, filters.

#### Element swap/edit protocol

When the user requests a change (e.g., "replace the person with X", "change the text to Y", "put a different background"):

1. **Lock all unchanged properties**: Preserve every visual property listed above EXCEPT the element being swapped.
2. **Describe the replacement**: Write the new element with the same level of detail as the original analysis.
3. **Maintain spatial consistency**: The replacement must occupy the same position, scale, and spatial relationship within the composition.
4. **Match lighting and color**: The replacement must receive the same lighting direction, color temperature, shadow behavior, and color grading as the original element.
5. **Output two prompts**: The original faithful prompt AND the modified prompt with the swap applied.

#### Output format

- **Always display the prompt on screen** in a clean, copy-ready format.
- **If a project directory is active**, also save to `<project_dir>/image_prompt_<timestamp>.txt`.
- **If no project directory**, present the prompt as copyable text only.
- Use the user's preferred language for explanations; write the generation prompt in English unless the user specifies otherwise.

#### Prompt structure skeleton

```text
[IMAGE GENERATION PROMPT — Reverse-Engineered from Source Image]

DIMENSIONS & FORMAT: [width]×[height] px, [aspect ratio], [orientation]
VISUAL MEDIUM: [exact style and sub-style]
CAMERA/LENS: [focal length estimate, DOF, aperture, lens character]

COMPOSITION: [framing rule, subject placement, horizon, leading lines, negative space]

LIGHTING:
- Primary: [direction, quality, color temp]
- Secondary: [fill/rim/accent lights]
- Effects: [volumetric, lens flare, caustics, shadows]

COLOR PALETTE: [dominant colors, harmony, saturation, contrast, grading style]

SUBJECTS:
- [Subject 1]: [exhaustive description with pose, expression, gaze, features]
- [Subject 2]: [if applicable]

WARDROBE & STYLING: [per-subject garment and accessory breakdown]

ENVIRONMENT: [setting, background layers, surfaces, atmospheric effects]

TEXT/TYPOGRAPHY: [exact text, font style, placement, effects] (if applicable)

MOOD & ATMOSPHERE: [emotional tone, energy, genre feel]

POST-PROCESSING: [filters, grain, vignette, effects]

NEGATIVE PROMPT: [what to explicitly avoid/exclude]
```

---

### 17. REEL ANALYSIS — Frame-by-Frame Video Decomposition Engine (v8.0)

Decomposes any video reel into a granular, time-coded analysis at approximately **3 captures per second** (~every 0.33s), with automatic scene-cut detection, segment grouping, and interconnected analysis suitable for AI video reproduction, content strategy analysis, or editorial study.

#### When to use
- The user uploads a video reel and wants it analyzed for AI reproduction.
- The user wants to understand a reel's editing strategy, pacing, camera work, or visual style.
- The user needs frame-by-frame reference data for recreating or adapting a video concept.

#### Analysis protocol

1. **Frame Extraction**: Extract frames at ~3 per second (configurable). Use `scripts/analyze_reel.py` when running locally, or describe the analysis inline when the video is provided as a reference.

2. **Scene-Cut Detection**: Automatically detect hard cuts, dissolves, and major transitions using histogram correlation. Mark every detected cut with a 🔪 marker.

3. **Segment Grouping**: Group consecutive frames between cuts into labeled segments (S1, S2, S3...). Each segment represents one continuous shot.

4. **Per-Frame Analysis** (for each captured frame):
   - **Timestamp**: Exact timecode (MM:SS.mmm)
   - **Shot Type**: Extreme wide, wide, medium, medium close-up, close-up, extreme close-up, macro, insert, over-shoulder, POV, aerial/drone, low-angle, high-angle, Dutch angle
   - **Camera Movement**: Static, pan L/R, tilt U/D, dolly in/out, truck L/R, crane up/down, Steadicam, handheld, zoom in/out, rack focus, whip pan, orbital
   - **Lens Estimate**: Focal length range and DOF character
   - **Lighting**: Direction, quality, Kelvin estimate, key-to-fill ratio
   - **Color Palette**: Dominant tones, grading style, saturation
   - **Subject & Action**: Who/what is in frame, what they're doing, body language, expression, movement vector
   - **Text/Overlay**: Any on-screen text, motion graphics, lower thirds, subtitles
   - **Audio Sync**: Music beat alignment, SFX timing, voiceover, dialogue
   - **Transition**: How this frame connects to the next (continuation, cut, dissolve, wipe, etc.)

5. **Segment-Level Analysis** (for each shot/segment):
   - Duration and frame count
   - Camera pattern summary
   - Lighting and color consistency
   - Narrative function (hook, build, climax, resolution, CTA)
   - Mood and energy level

6. **Global Analysis** (for the entire reel):
   - **Shot Sequence Map**: Visual flow diagram of all segments
   - **Pacing & Rhythm**: Cut frequency, acceleration/deceleration, beat sync
   - **Camera Vocabulary**: Movement patterns used across the reel
   - **Color & Lighting Strategy**: How palette shifts serve the narrative
   - **Text & Graphics Strategy**: Typography, timing, and placement patterns
   - **Audio-Visual Sync**: How music, SFX, and cuts work together
   - **Hook Analysis**: What makes the first 1–3 seconds attention-grabbing
   - **Loop Potential**: Whether the reel loops seamlessly and how

7. **AI Reproduction Prompts**: For each segment, generate a ready-to-use AI video prompt (compatible with Veo, Kling, Runway, Sora) that captures all visual properties needed to reproduce that segment.

#### Output files (always saved)

All analysis is **always saved to persistent files**, never just displayed ephemerally:

```
<output_dir>/
├── frames/                    ← Extracted frame images (frame_0001.jpg, ...)
├── reel_analysis.md           ← Complete structured analysis with tables and sections
└── reel_prompts.txt           ← AI video reproduction prompts per segment
```

- `reel_analysis.md`: Contains video metadata, frame-by-frame table, segment summary, and all global analysis sections.
- `reel_prompts.txt`: Contains one complete AI video prompt skeleton per detected segment, with timecodes and reference frame filenames.
- Both files are self-contained and can be shared, archived, or used as input for further production work.

#### Interconnected analysis principle

Every element in the analysis is **linked and cross-referenced**:
- Each frame references its segment ID
- Each segment references its constituent frames
- AI prompts reference both the segment timecodes and specific frame filenames
- Transitions describe what comes before AND after
- The global analysis references specific segments and timestamps as evidence

This interconnection ensures the analysis can be used for:
- **AI video reproduction**: Generate each segment independently with continuity
- **Strategy analysis**: Understand WHY the reel works (pacing, hooks, emotional arc)
- **Style transfer**: Apply the reel's visual language to new content
- **Editorial learning**: Study professional editing and camera techniques

---

## Photorealistic Character Bible Sheet Workflow

Use this workflow whenever the user asks to create, design, or prepare image prompts for a film character. Create a separate character sheet and a separate image prompt for each principal character. The sheet is a production reference for identity continuity; it is not a frame from the finished movie.

### Reference and originality rules
- When a user supplies a character image, explicitly treat it as the identity/appearance reference if that is their intent. Preserve recognizable facial identity, age appearance, skin tone, hair, and other requested traits. Do not turn "make it original" into an unrelated replacement face; make originality changes to wardrobe, accessories, color blocking, silhouette, and other non-identity details unless the user asks to redesign the person.
- Preserve the character type and anatomy shown in the reference. For robots and machines, explicitly lock a fully mechanical/non-human head and body when that is the intended design; exclude human skin, human eyes, nose, lips, ears, beard, or a human face under a helmet. Never use an erroneous generated result as the new identity reference; return to the user's original reference image.
- If more than one reference image is supplied, state each role in the prompt (for example: Image 1 = identity reference; Image 2 = layout reference only). Never borrow identity, costume, logo, or distinctive protected design from a layout-only image.
- Distinguish screenplay facts from proposed production choices. Never present invented names, age, height, voice, appearance, or equipment as screenplay facts. If the user wants a complete profile and the script omits details, either ask for essential choices or mark useful defaults as proposed/inferred and keep them consistent across all character prompts.
- Do not promise that small cosmetic changes guarantee legal clearance. Aim for a distinct original design and avoid copying recognizable actors, branded designs, or named fictional characters.

### Character-sheet composition
- Default to one clean landscape 16:9 character-bible board per character, with a neutral light studio background and readable panel dividers. Use photorealistic live-action photography when realism is requested; do not substitute concept-art, illustration, or obvious CGI language.
- Include a profile column with the exact character name, role, age, height (only if known or clearly proposed), personality, and voice profile. Base voice on screenplay dialogue/direction; label an inferred voice profile as a production suggestion.
- Include the same character in four consistent views: full-body front, full-body back, left profile, and right profile; a large face close-up; and close-ups of signature wardrobe, props, gear, or anatomy relevant to the story. Keep identity, proportions, outfit, and prop locations consistent across panels.
- Make panel hierarchy and scale explicit so the face, full-body views, and important details remain inspectable. No cropped views, blank/black regions, extra people, or contradictory costume details.
- Request only short exact labels in the image. Image models may garble dense text; if text accuracy is essential, generate the visual board cleanly and typeset the profile text afterward rather than claiming guaranteed legibility.
- If the user supplies a target layout image, follow its structure while keeping the character reference image as the sole identity source.

### Prompt skeleton

```text
Create a highly photorealistic live-action CHARACTER BIBLE SHEET for [CHARACTER NAME].
Reference roles: [identity image and any layout-only reference]. Preserve the same identity across every panel.
Canvas/layout: complete landscape 16:9 board, neutral studio background, readable separated panels; profile column, large face close-up, full-body front/back/left-profile/right-profile views, and close-up details of signature wardrobe/equipment/props.
Profile text: [name, role, age, height, personality, voice; mark inferred or proposed values].
Identity lock: [specific invariant face/body traits].
Wardrobe and equipment: [fixed details and exact placement, consistent in every relevant panel].
Photorealism: real live-action actor or practical prop, natural skin/hair/material texture, physically accurate studio lighting; no illustration or obvious CGI.
Text: short exact headings only; do not invent additional copy.
Avoid: changed identity, inconsistent views, cropped panels, blank/black canvas, extra characters, logos, watermark, and unrequested props.
```

---

## Mode-Based Production Protocol

```
1. IDENTIFY THE REQUESTED DELIVERABLE --> Poster, character sheet, location sheet, screenplay/shot plan, storyboard, video prompt, image-to-prompt, reel analysis, or a requested combination.
2. CHECK THE RELEVANT SOURCES        --> Read only the supplied script/reference material needed for that deliverable; distinguish facts from inferred/proposed details.
3. FOLLOW THAT MODE                  --> A poster or identity sheet can be produced independently. For video, storyboard and inspect the board before writing the final video prompt. For image-to-prompt, analyze the image and output the prompt. For reel analysis, extract, analyze, and save output files.
4. VERIFY SCOPE AND CONTINUITY        --> Check exact names, appearance, scene action, timings, camera movement, image roles, language, aspect ratio, and generation cap as applicable.
5. DELIVER THE REQUESTED OUTPUT       --> Include the English prompt when requested and a concise upload list specifying each image's role. For image-to-prompt and reel analysis, always provide copy-ready output and save files when a project directory is active.
```

---

## Reference Documentation

- [`USER_GUIDE.md`](USER_GUIDE.md): Comprehensive Arabic/English master user manual covering all 17 pillars, lens catalogs, safety lexicon, practical case studies, and the two new modes (IMAGE-TO-PROMPT & REEL ANALYSIS).
- [`references/prompt_template.md`](references/prompt_template.md): Complete prompt templates, optical tables, sheet-driven video prompt formulas, and IMAGE-TO-PROMPT reverse engineering template.
- [`references/output_format.md`](references/output_format.md): Folder architecture, `prompts.txt` schema, `storyboard.xlsx` tracking, and reel analysis output structure.
- [`references/image_to_prompt_guide.md`](references/image_to_prompt_guide.md): Detailed guide for the IMAGE-TO-PROMPT mode with analysis dimensions, swap protocol, and examples.
- [`references/reel_analysis_guide.md`](references/reel_analysis_guide.md): Detailed guide for the REEL ANALYSIS mode with analysis protocol, segment mapping, and AI reproduction prompts.
- [`scripts/extract_bridge_frame.py`](scripts/extract_bridge_frame.py): Dual-mode automated bridge frame extractor (`--video` or `--sheet --panel N --format 16x9|9x16`).
- [`scripts/analyze_reel.py`](scripts/analyze_reel.py): Reel frame extractor with scene-cut detection and structured analysis template generator.
- [`scripts/requirements.txt`](scripts/requirements.txt): Python dependencies (`opencv-python`, `numpy`).
- [`references/examples/character_bible_example_marwan_salim.jpg`](references/examples/character_bible_example_marwan_salim.jpg): Illustrative character-bible render only; not a default identity.
