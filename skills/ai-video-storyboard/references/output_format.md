# Output Format — Folder Structure, Unified Prompts Contract & Marketing Assets (v7.0)

**Template note:** Bracketed values are project inputs. Any sample project details below (genre, character, clothing, weather, location, or asset) are illustrative only; replace them with approved source details and omit irrelevant fields.

## Choose Output Scope Before Creating Files

- A single poster, storyboard prompt, character sheet, location sheet, or video prompt is a standalone deliverable. Return only what the user requested; do not create a project tree or `prompts.txt` by default.
- Use the project folder architecture and unified `prompts.txt` package only when the user requests a production package or the active project explicitly uses that structure.
- A marketing poster is independent of the storyboard-to-video sequence. A character or location bible may serve as a reference for later work, but is not a required prerequisite unless the user requests that workflow.

## Project Folder Architecture

Create this standardized tree under the project root (e.g. `C:\motion\` or the active workspace):

```
<project_name>/
├── screenplay_master.md              <-- Full screenplay / viral reel script / commercial script
├── character_location_bible.md       <-- Locked positive DNA traits and negative constraints
├── storyboard.xlsx                   <-- Master tracking sheet for all 10-second segments & frames
├── _references/                      <-- Original anchor photos & extracted video faces
│   ├── [character_face_reference.jpg]
│   └── [location_environment_reference.jpg]
├── Thumbnails_and_Posters/           <-- Official promotional & marketing package
│   ├── The_[Title]_Thumbnail_16x9.jpg   <-- Widescreen YouTube / Facebook thumbnail (3D icy title)
│   ├── The_[Title]_Poster_Reels_9x16.jpg <-- Vertical theatrical poster for Reels / TikTok
│   └── social_media_captions.txt        <-- Bilingual (Arabic/English) copy with hashtags & CTAs
├── Scene01_Segment01_<shortname>/
│   ├── storyboard_sheet.jpg          <-- 4×3 Widescreen Sheet (or reels_sheet_01 & 02 for 9:16)
│   └── prompts.txt                   <-- UNIFIED MASTER PROMPT FILE (All-In-One, zero clutter)
├── Scene01_Segment02_<shortname>/
│   ├── bridge_frame.jpg              <-- Dual Bridge Frame (extracted via video or sheet crop)
│   ├── storyboard_sheet.jpg
│   └── prompts.txt                   <-- UNIFIED MASTER PROMPT FILE (Includes Spatial Audit)
└── ...
```

> [!IMPORTANT]
> **Zero File Clutter Policy**:
> We DO NOT generate separate `gemini_safe_prompt.txt` or `voice_profile_prompt.txt` files. Everything is cleanly synthesized into the **single master file: `prompts.txt`**.

---

## Unified `prompts.txt` Schema (v7.0)

When a segment prompt package is requested, each segment folder may contain one self-contained `prompts.txt` using the relevant sections below. Omit sections that do not apply to the requested deliverable; do not force the full package on a standalone image prompt.

```
================================================================================
CINEMATIC MOVIE PRODUCTION — MASTER PROMPT PACKAGE (v7.0)
Project: [PROJECT NAME] | Segment: [SEGMENT NAME & TIMECODES]
Aspect Ratio: [16:9 Widescreen / 9:16 Vertical Reels]
Target Models: Google Veo / Gemini Video / Kling AI / Runway Gen-3 / OpenAI Sora
Bridge Frame: Linked to Segment [PREV_SEGMENT] (`bridge_frame.jpg`)
================================================================================

--------------------------------------------------------------------------------
[NARRATIVE REALITY & CHARACTER DNA LOCK]
--------------------------------------------------------------------------------
- Production Mode: [User-requested project/genre and visual medium].
- Safety & Content Policy: [Apply the target platform's current rules where relevant; no prompt wording guarantees acceptance. Preserve the requested story and tone.]
- Character DNA (replace every bracket with approved source facts):
  * Identity: [name, role, age appearance, human/creature/robot as approved].
  * Facial Structure & Bone Anchor: [approved face shape, cheekbones, jawline].
    STRICT NEGATIVE: Do NOT render face as [list only unapproved variants relevant here]. [Include age lock only for approved adults.]
  * Hair & Eyes: [approved hair color/style, eyes].
  * Outerwear & Trim: [approved garments, colors, materials, exact placement].
    STRICT NEGATIVE: [only script-relevant exclusions, e.g. wrong trim color].
  * Accessories / Equipment: [approved items and where worn/held].
- Companion / Asset Mandate (only if the scene has one):
  * [approved species/object, temperament or condition, markings/props with exact placement].
- Lighting / visual invariants:
  * [Approved scene-specific palette, light direction, time of day, and exclusions; omit if not applicable.]

--------------------------------------------------------------------------------
[SPATIAL GEOMETRY & ANCHOR AUDIT]
--------------------------------------------------------------------------------
- Subject Postures: [Exact starting physical postures in bridge_frame.jpg].
- Hand Coordinates & Prop Anchor: [Exact coordinates of hands and props held].
- Spatial Reachability: [Distance from hand to target; verify <= 15% frame width or apply Medium Action Shot].
- Target Anatomical Localization: [Exact body part and screen quadrant].
- Spatial Negative Exclusions: [Explicitly barred neighboring anatomy, e.g. zero patches on neck or ears].
- Prop Hand Transition: [Hand release state, anti-duplication directive].

--------------------------------------------------------------------------------
PART 1: MASTER STORYBOARD SHEET PROMPT (Image Generation — Step 1)
--------------------------------------------------------------------------------
[Complete prompt for generating the 4x3 Widescreen Sheet or Dual 5+5 Vertical Reels Sheets,
 including circled panel numbers ① to ⑩, camera directions, and technical slate cards].

--------------------------------------------------------------------------------
PART 2: INSTANT STORYBOARD-TO-VIDEO ENGINE PROMPT (Built LAST after auditing sheet)
--------------------------------------------------------------------------------
[CRITICAL ZERO-GRID MANDATE — INSTANT FULL-SCREEN LIVE ACTION AT 0:00S]:
From the very first frame at 0.00 seconds, the video MUST BE 100% FULL-SCREEN LIVE ACTION CINEMA.
STRICT NEGATIVE: ABSOLUTELY DO NOT SHOW THE STORYBOARD SHEET, DO NOT SHOW THE 12-PANEL GRID, DO NOT SHOW WHITE OR BLACK FRAMES/BORDERS, AND DO NOT DISPLAY TEXT CAPTIONS IN THE FIRST SECOND!

[SAFETY & PRODUCTION FRAMEWORK]:
[OPTIONAL: use fictional-production/staged-action context only if it fits the project. Preserve the requested genre, action, and stakes; do not claim this wording guarantees platform acceptance.]

[CAMERA & DIRECTING MODE]:
[Mode A: Steadicam Unidirectional Vector (Follow/Lead shot with zero spinning) OR Mode B: Hollywood Cinematic Coverage Cuts].

[CHOREOGRAPHY & SECOND-BY-SECOND MILESTONES]:
- Seconds 0:00–0:02: [Panels 1 & 2 Action].
- Seconds 0:02–0:04: [Panels 3 & 4 Action].
- Seconds 0:04–0:06: [Panels 5 & 6 Action].
- Seconds 0:06–0:08: [Panels 7 & 8 Action].
- Seconds 0:08–0:10: [Panels 9 & 10 Action + Destination Reveal].

[CONTINUITY & INVARIANTS]:
- 180° Axis lock, Character DNA lock, prop/marking persistence per script.
- Weather/atmosphere dynamics: only scripted effects, continuous across the unit.
- Atmosphere & Lighting: approved Kelvin/palette and volumetric treatment.

--------------------------------------------------------------------------------
PART 3: SEQUENTIAL SECOND-BY-SECOND BREAKDOWN (Frames 01 to 10)
--------------------------------------------------------------------------------
[Second-by-second breakdown for micro-generation or VFX artists:
 Each second includes: Visual, Camera Optics, Lighting Kelvin, Motion Vectors, Dialogue & Mix].

--------------------------------------------------------------------------------
PART 4: DIRECTOR'S LOGICAL & PHYSICAL SANITY AUDIT
--------------------------------------------------------------------------------
[Formal 5-point verification report:
 1. Spatial Axis & 180° Eyeline Rule: [PASSED]
 2. Spatial Reachability & Feasibility: [PASSED]
 3. Planar Surface Interaction & Anti-Toroidal Physics: [PASSED]
 4. Prop Anti-Duplication & Hand State Transitions: [PASSED]
 5. Asset & Environmental Persistence (Wound, wardrobe, weather): [PASSED]]
```

---

## Master Production Excel Ledger (`storyboard.xlsx`)

The workbook `storyboard.xlsx` tracks the entire production across two official sheets:

### Sheet 1: `Overview`
High-level tracking of all 10-second segments across all episodes.

| Column | Header | Description |
|---|---|---|
| A | `Scene #` | Scene number (e.g. 1, 2, 5, 8). |
| B | `Scene Title` | Descriptive dramatic title of the scene. |
| C | `Segment #` | Monotonic segment index (1 to 18). |
| D | `Segment Range` | Exact timecodes (e.g. `0:00-0:10`, `1:10-1:20`). |
| E | `Setting` | Environmental location and lighting. |
| F | `Characters` | Character names present in segment. |
| G | `Tone` | Emotional and dramatic tone. |

### Sheet 2: `Frames`
Granular tracking of all individual seconds (Frames 01 to 10 of each segment).

| Column | Header | Description |
|---|---|---|
| A | `Scene #` | Scene number. |
| B | `Scene Title` | Dramatic title. |
| C | `Segment #` | Segment number. |
| D | `Segment Range` | Timecode range. |
| E | `Frame #` | Second index within segment (1 to 10). |
| F | `Timestamp` | Exact video timecode (e.g. `1:14`). |
| G | `Batch` | Grouping or render batch index. |
| H | `Visual Summary` | 1-line description of the visual frame. |
| I | `Camera` | Focal length, shot size, and camera movement. |
| J | `Dialogue` | Exact spoken lines or `None`. |
| K | `Music/SFX` | Foley, breath sounds, and musical score cues. |
| L | `Folder Path` | Relative directory path. |
| M | `Status` | `Video Generated` / `Master Sheet Ready & Verified`. |
