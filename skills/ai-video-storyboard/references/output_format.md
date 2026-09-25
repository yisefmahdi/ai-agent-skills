# Output Format — Folder Structure, Unified Prompts Contract & Marketing Assets (v4.0)

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

## Unified `prompts.txt` Schema (v4.0)

Each segment folder contains a single self-contained `prompts.txt` following this exact 6-tier structure:

```
================================================================================
CINEMATIC MOVIE PRODUCTION — MASTER PROMPT PACKAGE (v4.0)
Project: [PROJECT NAME] | Segment: [SEGMENT NAME & TIMECODES]
Aspect Ratio: [16:9 Widescreen / 9:16 Vertical Reels]
Target Models: Google Gemini Video / Kling AI / Runway Gen-3
Bridge Frame: Linked to Segment [PREV_SEGMENT] (`bridge_frame.jpg`)
================================================================================

--------------------------------------------------------------------------------
[NARRATIVE REALITY & CHARACTER DNA LOCK]
--------------------------------------------------------------------------------
- Production Mode: Scripted Cinematic Family Adventure Drama.
- Safety & Content Policy: 100% compliant with Google Gemini AI Safety Guidelines. 
  (Framed as an authorized studio film set with professional stunts and theatrical prop makeup).
- Character DNA:
  * Identity: [e.g. Young female explorer, early 20s, sole human in scene].
  * Facial Structure: [e.g. Slender elongated oval face, delicate pointed chin, fair skin].
    STRICT NEGATIVE: Do NOT render face as round, wide, puffy, or square.
  * Hair & Eyes: [e.g. Dark brunette, natural eyebrows, hazel eyes].
  * Outerwear & Trim: [e.g. Vivid matte red insulated parka, light-brown coyote fur hood trim].
    STRICT NEGATIVE: Fur trim must NEVER be black, dark gray, or synthetic neon.
  * Accessories: [e.g. Clear ski goggles pushed up securely on forehead, black snow pants, black gloves].
- Companion / Asset Mandate:
  * [e.g. Docile young adult cream polar bear with PROMINENT distinct circular reddish injury patch on front-left shoulder fur facing the camera].
- Negative Lighting Invariant:
  * [STRICT NEGATIVE: Absolutely NO sunlight, NO direct sun, NO golden hour, NO sunbeams, NO sunset glow, NO yellow/orange horizon tints. 100% cold diffused overcast daylight].

--------------------------------------------------------------------------------
[SPATIAL GEOMETRY & ANCHOR AUDIT] (New in v4.0)
--------------------------------------------------------------------------------
- Subject Postures: [Exact starting physical postures in bridge_frame.jpg].
- Hand Coordinates & Prop Anchor: [Exact coordinates of hands and props held].
- Spatial Reachability: [Distance from hand to target; verify <= 20% frame width or apply Medium Action Shot].
- Target Anatomical Localization: [Exact body part and screen quadrant].
- Spatial Negative Exclusions: [Explicitly barred neighboring anatomy, e.g. zero bandages on neck or ears].
- Prop Hand Transition: [Hand release state, anti-duplication directive].

--------------------------------------------------------------------------------
PART 1: MASTER STORYBOARD SHEET PROMPT (Image Generation)
--------------------------------------------------------------------------------
[Complete prompt for generating the 4x3 Widescreen Sheet or Dual 5+5 Vertical Reels Sheets,
 including circled panel numbers ① to ⑩, camera directions, and technical slate cards].

--------------------------------------------------------------------------------
PART 2: INSTANT VIDEO ENGINE PROMPT (Ready-to-Paste for Gemini / Kling / Runway)
--------------------------------------------------------------------------------
[The complete, copy-pasteable, safety-shielded prompt featuring:
 1. Reference Image Continuity & Character Identity Lock (Zero Morphing)
 2. Critical 180° Axis & Target Localization (Wound facing camera)
 3. Spatial Negative Exclusion Lock (No stray props on neighboring anatomy)
 4. Strict Atmosphere & Negative Lighting Lock (Overcast, no sun)
 5. Single Unbroken Continuous Steadicam/Dolly Take
 6. Planar Direct Interaction Steps (Anti-Toroidal; zero 3D wrapping)
 7. Prop Release & Anti-Duplication Mechanics
 8. Embedded Dialogue & Vocal Performance Timing
 9. Wholesome Cinematic Drama Style Profile]

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