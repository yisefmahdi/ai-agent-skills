# Output Format — Folder Structure, Unified Prompts Contract & Marketing Assets (v3.0)

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
│   └── prompts.txt                   <-- UNIFIED MASTER PROMPT FILE
└── ...
```

> [!IMPORTANT]
> **Zero File Clutter Policy**:
> We DO NOT generate separate `gemini_safe_prompt.txt` or `voice_profile_prompt.txt` files. Everything is cleanly synthesized into the **single master file: `prompts.txt`**.

---

## Unified `prompts.txt` Schema

Each segment folder contains a single self-contained `prompts.txt` following this exact 5-tier structure:

```
================================================================================
CINEMATIC MOVIE PRODUCTION — MASTER PROMPT PACKAGE
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
PART 1: MASTER STORYBOARD SHEET PROMPT (Image Generation)
--------------------------------------------------------------------------------
[Complete prompt for generating the 4x3 Widescreen Sheet or Dual 5+5 Vertical Reels Sheets,
 including circled panel numbers ① to ⑩, camera directions, and technical slate cards].

--------------------------------------------------------------------------------
PART 2: INSTANT VIDEO ENGINE PROMPT (Ready-to-Paste for Gemini / Kling / Runway)
--------------------------------------------------------------------------------
[The complete, copy-pasteable, safety-shielded prompt featuring:
 1. Reference Image Continuity & Character Identity Lock (Zero Morphing)
 2. Critical Visual Mandate / Asset Orientation (Wound facing camera)
 3. Strict Atmosphere & Negative Lighting Lock (Overcast, no sun)
 4. Single Unbroken Continuous Steadicam/Dolly Take (No sudden cuts or close-up zooms)
 5. Embedded Dialogue & Vocal Performance Timing
 6. Wholesome Cinematic Drama Style Profile]

--------------------------------------------------------------------------------
PART 3: SEQUENTIAL SECOND-BY-SECOND BREAKDOWN (Frames 01 to 10)
--------------------------------------------------------------------------------
[Second-by-second breakdown for micro-generation or VFX artists:
 Each second includes: Visual, Camera Optics, Lighting Kelvin, Motion Vectors, Dialogue & Mix].

--------------------------------------------------------------------------------
PART 4: DIRECTOR'S LOGICAL & PHYSICAL SANITY AUDIT
--------------------------------------------------------------------------------
[Formal 4-point verification report:
 1. Spatial Axis & 180° Eyeline Rule: [PASSED]
 2. Kinematic & Gravitational Sanity: [PASSED]
 3. Asset & Environmental Persistence (Wound, wardrobe, weather): [PASSED]
 4. Anti-Hallucination Completeness (Single-actor isolation, no extra limbs): [PASSED]]
```

---

## Dual Bridge Frame Automation

To transition between segments, run the automated Python helper script:

```bash
# Path A: When MP4 video has been rendered and saved locally
python scripts/extract_bridge_frame.py --video "path/to/Segment_N.mp4" --out "path/to/Segment_N+1/bridge_frame.jpg"

# Path B: Fallback when working with images only (no local video file)
python scripts/extract_bridge_frame.py --sheet "path/to/Segment_N/storyboard_sheet.jpg" --out "path/to/Segment_N+1/bridge_frame.jpg" --format 16x9
```

---

## Master Tracking Sheet (`storyboard.xlsx`) Columns

Maintain project-wide continuity using these 12 columns in `storyboard.xlsx`:

1. `Segment`: Segment ID (e.g. `Segment 01`).
2. `Timecode`: Timestamp range (e.g. `0:00–0:10`).
3. `Second`: Second index (e.g. `0:00`).
4. `Frame_ID`: Frame identifier (e.g. `01`).
5. `Shot_Type`: Shot scale and optic (e.g. `Wide Shot, 24mm`).
6. `Camera_Movement`: Rig and motion vector (e.g. `Steadicam tracking forward`).
7. `Action_Description`: Detailed physical action, Newtonian kinematics.
8. `Lighting_Kelvin`: Color temperature and weather (e.g. `6500K overcast`).
9. `Dialogue`: Spoken lines and timecodes.
10. `Audio_SFX`: Foley, wind resistance, breath sound.
11. `Bridge_Status`: `Anchor Frame`, `Internal Frame`, or `Handoff Outro`.
12. `Generation_Status`: `Draft`, `Sheet_Generated`, `Video_Rendered`, `Approved`.