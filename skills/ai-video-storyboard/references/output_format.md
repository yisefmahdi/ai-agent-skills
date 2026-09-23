# Output Format — Folder Structure, Prompts Format, Voice DNA & Excel Schema

## Folder structure

Create this tree under the project directory (e.g. `C:\motion\` or project root):

```
<project_name>/
├── storyboard.xlsx
├── full_script_master.txt
├── character_location_bible.md
├── _references/
│   ├── [character_real_reference_image.jpg]
│   └── [location_reference_image.jpg]
├── Scene01_Segment01_<shortname>/
│   ├── storyboard_sheet.jpg          <-- Generated 5×2 contact sheet
│   ├── prompts.txt                   <-- DNA lock + Sheet prompt + 10 video prompts + Logic Audit
│   └── voice_profile_prompt.txt      <-- Persistent vocal fingerprint & sound mix
├── Scene01_Segment02_<shortname>/
│   ├── bridge_frame.jpg              <-- Direct copy of Segment 01's Frame 10 (MANDATORY)
│   ├── storyboard_sheet.jpg
│   ├── prompts.txt                   <-- Bridge frame anchor + DNA lock + Sheet + Video prompts + Logic Audit
│   └── voice_profile_prompt.txt
├── Scene02_Segment03_<shortname>/
│   ├── bridge_frame.jpg              <-- Direct copy of Segment 02's Frame 10
│   ├── storyboard_sheet.jpg
│   ├── prompts.txt
│   └── voice_profile_prompt.txt
└── ...
```

---

## prompts.txt format (inside each segment folder)

Each `prompts.txt` follows this standardized five-tier structure:

```
================================================================================
SEGMENT 02 — Scene 1: The Descent — 0:10–0:20
Format: Master Storyboard Sheet (5 Columns × 2 Rows = 10 Panels)
Target Video Aspect Ratio: 16:9
Bridge Frame: Linked to Segment 01 [FRAME 10]
================================================================================

--------------------------------------------------------------------------------
[NARRATIVE REALITY & GENRE PROFILE]
--------------------------------------------------------------------------------
- Genre: Photorealistic Cinematic Survival Thriller.
- Physics Baseline: Strict Newtonian physics (gravity, inertia, air resistance).
- Weather Kinetics: High-velocity sub-zero gale winds (~50 knots), atmospheric frost, breath condensation.
- Safety Framing: Fictional cinematic stunt sequence, professional stunt blocking, zero graphic harm.

--------------------------------------------------------------------------------
[CHARACTER & ASSET DNA LOCK] (MANDATORY CONSISTENCY SPECIFICATION)
--------------------------------------------------------------------------------
- Character: Young woman, early 20s.
- Face Geometry: Slim elongated oval facial structure, delicate pointed chin, fair skin with cold-flushed cheeks, natural dark eyebrows. (STRICT NEGATIVE: Do NOT make face wide, round, or square).
- Eyes: Expressive hazel-brown, clear pupils.
- Hair: Dark brunette, fine strands peeking out around forehead and neck.
- Wardrobe: Heavy insulated expedition parka in vivid matte crimson red.
- Hood Trim: Fluffy light-brown/tan frosted coyote fur trim. (STRICT NEGATIVE: Fur must NEVER be black, gray, or synthetic neon).
- Gear: Clear alpine goggles pushed up onto forehead; dark charcoal thermal climbing gloves.
- Atmosphere/Environment: Harsh Antarctic sub-zero glacier, overcast cold daylight (~6500K), volumetric snow flurry drifting from left to right.

--------------------------------------------------------------------------------
[BRIDGE FRAME CONTINUITY SPECIFICATION]
--------------------------------------------------------------------------------
Frame 01 of this segment is the DIRECT CONTINUATION of Segment 01 Frame 10.
- Starting Physical State: Subject grips the metal door handle of the tilting cabin, body angled 25 degrees outward.
- Camera Position: Static low angle looking outward past her shoulder, matching Segment 01 Frame 10 exactly.
- Action Momentum: Motion resumes from the exact millisecond of the door swing.

--------------------------------------------------------------------------------
PART 1: MASTER STORYBOARD SHEET PROMPT (Image Generation)
--------------------------------------------------------------------------------
Prompt:
Professional cinematic production storyboard sheet, formatted as a 5-column by 2-row grid containing 10 sequential widescreen panels with clean white borders and gutters.
Header at top left: 'SCENE TITLE: "The Descent - Loss of Control" | SEGMENT 02 (0:10 - 0:20)'
Header at top right: 'PAGE: 2 OF 6'
Style: Realistic cinematic film illustration style, highly detailed, dramatic lighting, technical camera captions below each panel.

ROW 1 (TOP ROW - Seconds 0:10 to 0:15):
- Panel 1: (Circled number ① in upper left corner). [BRIDGE FRAME CONTINUATION]. Wide shot cabin interior...
  [Caption: BRIDGE FRAME - CABIN EQUILIBRIUM LOST. CAMERA: 24MM LOW ANGLE TILT. LIGHTING: 6500K COLD OVERCAST.]
- Panel 2: (Circled number ② in upper left corner)...
- Panel 3: (Circled number ③ in upper left corner)...
- Panel 4: (Circled number ④ in upper left corner)...
- Panel 5: (Circled number ⑤ in upper left corner)...

ROW 2 (BOTTOM ROW - Seconds 0:15 to 0:20):
- Panel 6: (Circled number ⑥ in upper left corner)...
- Panel 7: (Circled number ⑦ in upper left corner)...
- Panel 8: (Circled number ⑧ in upper left corner)...
- Panel 9: (Circled number ⑨ in upper left corner)...
- Panel 10: (Circled number ⑩ in upper left corner). [OUTRO ANCHOR FOR NEXT SEGMENT]...

--------------------------------------------------------------------------------
PART 2: SEQUENTIAL 10-SECOND VIDEO GENERATION PROMPTS (Frames 01 to 10)
--------------------------------------------------------------------------------

[FRAME 01 — 0:10] (BRIDGE FRAME — 100% VISUAL CARRYOVER FROM SEGMENT 01 FRAME 10)
VISUAL: [Inherits locked Character DNA: red parka, light-brown coyote fur hood, slim oval face]. Exact starting posture from Segment 01 Frame 10: gripped onto the cabin door latch, snow blowing into her face.
CAMERA: 35mm lens, low angle looking past shoulder, handheld shoulder-rig micro-shudder, static framing resuming motion. Depth of field f/2.8.
LIGHTING: Cool diffused daylight (~6500K), rim light off ice sheet below, subtle cold skin reflections.
MOTION/TRANSITION: Hand slips 1 inch along the railing; body sways outward by 5 degrees; hair strands flutter forward at 45 degrees.
DIALOGUE: "!ما بقدر أتمسك أكتر"
VOICE TONE: Screamed over roaring blizzard wind, desperate vocal fry.
MUSIC/SFX: High-wind howl, metal screeches against rotor turbulence.
ASPECT RATIO: 16:9
CONTINUITY: 100% match with Segment 01 Frame 10 image. No clothing, hair, or facial changes allowed.

[FRAME 02 — 0:11]
...

--------------------------------------------------------------------------------
[DIRECTOR'S LOGICAL & PHYSICAL SANITY AUDIT]
--------------------------------------------------------------------------------
1. Spatial & 180° Axis Consistency:
   [PASSED] The helicopter's tilt and flight direction remain consistent Screen-Left to Screen-Right across all 10 frames. No jarring reverse-angle disorientations.
2. Kinematic & Gravitational Sanity:
   [PASSED] When the cabin tilts right, loose equipment and the character's body naturally slide rightward under gravity. Wind forces blow loose hair and fur in a uniform vector.
3. Progressive Anatomy & Asset Continuity:
   [PASSED] Light-brown coyote fur trim is maintained in 100% of frames. Face remains slim with delicate chin. Goggles stay firmly anchored above forehead without teleporting.
4. Zero-Hallucination Specificity Score:
   [100% Microscopic Precision] Every second specifies exact limb placements, lighting Kelvin, and lens focal lengths, eliminating model guesswork.
```

---

## voice_profile_prompt.txt format (inside each segment folder)

```
================================================================================
STRICT VOCAL DNA & ACOUSTIC PROFILE — SEGMENT 02 (0:10 - 0:20)
Character: [Character Name]
================================================================================

1. CHARACTER VOCAL FINGERPRINT:
- Perceived Age: Female, early 20s (approx 22).
- Native Timbre: Clear, natural, warm mid-range soprano with slight rasp under physical strain.
- Shiver & Thermal Resonance: Sub-zero acoustic coloring — trembling diaphragm, short rapid breath intakes between syllables, audible teeth chatter when pausing.
- Speech Cadence: Urgent, irregular rhythm dictated by adrenaline and g-force.

2. SECOND-BY-SECOND DIALOGUE & VOCAL PERFORMANCE:
- [0:10 - 0:12] (Frames 01–02):
  Spoken Line: "!ما بقدر أتمسك أكتر"
  Delivery: Desperate yell, strained throat vocal fry, pushed to the top of her vocal register to overcome rotor thunder.
- [0:13 - 0:15] (Frames 03–05):
  Spoken Line: [Involuntary sharp gasp: "Ah!"]
  Delivery: Sudden sharp inhalation, airflow choked by sudden free-fall sensation.
- [0:16 - 0:18] (Frames 06–08):
  Spoken Line: "لا... لاااا!"
  Delivery: Screamed vocalization trailing into Doppler-effect fade as distance increases.
- [0:19 - 0:20] (Frames 09–10):
  Spoken Line: [Silence / wind roaring]
  Delivery: Heavy rushed air intake over microphone.

3. SOUND ENGINEERING & MIX RATIOS:
- Voice Clarity: 60% prominent in mix, centered stereo.
- Environmental Ambience: 30% howling Antarctic blizzard wind (heavy low-frequency rumble + high whistling).
- Mechanical SFX: 10% distant stuttering helicopter turbine.
- Lip-Sync Anchor: Wide mouth opening on "!أكتر" (Frames 01-02), rapid jaw snap shut on gasp (Frame 03).
```

---

## storyboard.xlsx schema

| Column | Description / Example |
|---|---|
| **Scene #** | e.g. `1` |
| **Scene Title** | e.g. `"The Descent"` |
| **Segment #** | Global segment number, e.g. `2` |
| **Segment Timerange** | e.g. `"0:10–0:20"` |
| **Frame #** | `1` to `10` |
| **Bridge Frame?** | `"Yes (Anchor from Seg 01)"` (for Frame 01), else `"No"` |
| **Sheet Panel** | `"Panel ① (Row 1, Col 1)"`, `"Panel ⑥ (Row 2, Col 1)"` |
| **Timestamp** | `"0:10"`, `"0:11"`, etc. |
| **Visual Summary** | 1-line action summary with locked DNA check |
| **Camera & Lens** | e.g. `"35mm anamorphic, low angle tilt, f/2.8"` |
| **Lighting (Kelvin)** | e.g. `"6500K overcast, cold rim light"` |
| **Dialogue** | Spoken line or blank |
| **Voice Profile Cue** | Delivery note (e.g. `"Strained scream, vocal fry"`) |
| **Logic Verified?** | `"PASSED (Kinematics & Eyeline OK)"` |
| **Folder Path** | Relative path, e.g. `Scene01_Segment02_TheDescent/` |
| **Status** | `Prompt Ready / Sheet Rendered / Video Generated` |