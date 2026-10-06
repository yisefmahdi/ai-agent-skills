# REEL ANALYSIS — Frame-by-Frame Video Decomposition Guide (v8.0)

> This guide is the official technical reference for the **REEL ANALYSIS** mode of the `ai-video-storyboard` skill (v8.0). It defines the frame extraction protocol (~3 captures/second), scene-cut detection, kinematic & optical decomposition, narrative rhythm auditing, and synthesis into AI video reproduction prompts.

---

## Purpose & Overview

The **REEL ANALYSIS** engine dissects high-performing short-form video reels (Instagram Reels, TikTok, YouTube Shorts, commercial micro-spots) down to granular sub-second intervals (~0.33s / 3 frames per second).

It serves two primary workflows:
1. **AI Video Reproduction / Re-creation**: Deconstructing a viral or reference video to recreate it identically—or with customized swapped subjects, branding, environment, or narrative elements—using generative AI tools (Google Veo, Kling 1.5/Pro, Runway Gen-3 Alpha, OpenAI Sora, MiniMax Hailuo).
2. **Strategic & Editorial Deconstruction**: Revealing why a video retains attention by mapping visual pacing, hook mechanics, camera movements, typography beats, and audio-visual synchronization.

---

## Core Protocol: The 3 Captures-Per-Second Standard

Human perception processes video cuts and micro-actions in roughly 200–400ms windows. By sampling at **3 frames per second (fps)** (every ~0.33 seconds):
- No fast whip-pan, micro-cut, or typography pop is missed.
- The data volume remains manageable and inspectable without drowning in redundant 24/30/60fps video packets.
- Transitions and momentum arcs are mapped with mathematical precision.

### Automated Tooling: `scripts/analyze_reel.py`

Run the included extractor script:
```powershell
python C:\AI\SKILL\ai-video-storyboard\scripts\analyze_reel.py --video "C:\path\to\reel.mp4" --out "C:\path\to\output_dir" --fps 3
```

The script automatically:
1. Extracts frames to `frames/frame_0001.jpg`, `frame_0002.jpg`, etc.
2. Identifies scene cuts using HSV color histogram correlation ($< 0.55$).
3. Generates the structured `reel_analysis.md` audit sheet.
4. Prepares `reel_prompts.txt` populated with prompt templates per detected segment.

---

## The 9-Stage Decomposition Architecture

### Stage 1: File & Metadata Telemetry
- **Video dimensions**: e.g., $1080 \times 1920$ (9:16 Vertical) or $1920 \times 1080$ (16:9 Widescreen).
- **Native frame rate**: e.g., 29.97, 30, or 60 fps.
- **Duration**: Exact down to centiseconds (e.g., 14.82s).
- **Sampling interval**: 3 captures/second ($\Delta t \approx 0.33\text{s}$).

### Stage 2: Scene Cut & Segment Mapping
- Consecutive frames between cuts form a **Segment ($S1, S2, S3 \dots$)**.
- Mark cuts with type: **Hard Cut**, **Match Cut**, **Whip Pan / Whip Cut**, **Speed Ramp Dissolve**, **Zoom / Morph Transition**, or **Invisible Object Wipe**.
- Duration of each segment in seconds and frame count.

### Stage 3: Sub-Second Frame Audit (The Frame Matrix)
Each sampled frame is classified across these dimensions:

| Dimension | Parameters Evaluated |
| :--- | :--- |
| **Shot Scale** | Extreme Wide (EWS), Wide (WS), Full (FS), Medium (MS), Medium Close-Up (MCU), Close-Up (CU), Extreme Close-Up (ECU), Macro |
| **Camera Angle** | Eye-Level, Low Angle, High Angle, Worm's Eye, Bird's Eye, Dutch / Canted Angle |
| **Camera Motion** | Static, Push-In (Dolly In), Pull-Out, Pan (L/R), Tilt (U/D), Truck (L/R), Boom/Jib, Orbit/Arc, Handheld Jitter, Steadicam Glide, Crash Zoom |
| **Lens Optics** | Ultra-wide anamorphic, standard 35/50mm, 85mm portrait, shallow DOF bokeh, deep focus |
| **Lighting & Kelvin** | Direction (key, fill, rim, silhouette), Quality (hard, diffused), Kelvin range (e.g., 3200K warm vs 7500K cool), Specular flares |
| **Color Grading** | Contrast grade, saturation, shadow tint, highlight rolloff, dominant hex tones |
| **Subject Choreography** | Anatomy pose, facial micro-expression, gaze vector, hand gestures, speed vector |
| **Text & Graphics** | Captions, animated stickers, kinetic typography, brand badges, emojis, screen position |
| **Audio Synchrony** | Bass drop, snare snap, riser crescendo, voiceover punchline, silence gap |

### Stage 4: Rhythm & Pacing Heatmap
- **Pacing Curve**: Calculate Average Shot Length (ASL) across segments.
- **Velocity Shifts**: Fast-paced rapid-fire editing (0.3s–0.8s cuts) vs. slow lingering payoff shots (2.0s–4.0s).
- **Retention Bridge Analysis**: What happens precisely between Second 0:01 and 0:04 to arrest scrolling inertia.

### Stage 5: Lighting & Palette Continuity Engine
- Document whether the reel maintains uniform color science throughout or deliberately changes palettes per scene to signal emotional shifts or flashbacks.

### Stage 6: Camera Choreography Grammar
- Group movements into a unified spatial vocabulary (e.g., "alternating push-in and truck-left" or "consistent continuous Steadicam follow").

### Stage 7: Typography & UI Overlay Tracking
- Timecode start and end of every caption.
- Font styling, weight, color contrast, and safe-zone compliance (avoiding Instagram/TikTok UI buttons on the right margin).

### Stage 8: Sound Design & Foley Synchronization
- Alignment of audio markers (SFX whooshes, impacts, risers) with exact video frame timestamps.

### Stage 9: AI Video Generation Prompt Translation
Translate each continuous segment into a dedicated AI video generation prompt structured for modern models (Veo, Kling, Runway Gen-3, Sora).

---

## AI Reproduction Prompt Formula (Per Segment)

When writing reproduction prompts for segments in `reel_prompts.txt`:

```text
================================================================================
SEGMENT S[##] — AI VIDEO GENERATION PROMPT
Timecode: [00:00.000] - [00:00.000] (Duration: [X.XX]s) | Aspect Ratio: [9:16 / 16:9]
Reference Anchor Frames: [frame_XXXX.jpg]
================================================================================

[INSTANT ACTION & FULL-SCREEN LIVE ACTION AT 0:00S]:
Render full-screen cinema live-action from Frame 0. Zero UI, zero borders, zero watermarks.

[CAMERA & OPTICAL SPECIFICATION]:
- Shot Type: [Shot scale, e.g. Low-angle Medium Close-Up]
- Lens / Focal Length: [e.g. 35mm Anamorphic T2.4, subtle barrel distortion]
- Depth of Field: [e.g. Shallow DOF with creamy background separation]
- Camera Vector / Movement: [e.g. Smooth forward dolly push-in at constant 1.2m/s with zero rotation]

[SUBJECT & KINEMATIC CHOREOGRAPHY]:
- Subject: [Precise description of person/object: age, anatomy, clothing, expression]
- Action: [Exact mechanical motion beat-by-beat across the segment duration]
- Eye line & Gaze: [Direction of sight relative to lens]

[LIGHTING, KELVIN & COLOR SCIENCE]:
- Key Light: [Direction, intensity, quality]
- Color Temperature: [e.g. 5600K clean balanced daylight with subtle 3200K tungsten backlight]
- Color Grade: [e.g. High-contrast cinematic contrast, rich deep blacks, balanced skin tones]

[ATMOSPHERE & PARTICULATE DYNAMICS]:
- Environmental particles: [e.g. subtle atmospheric dust motes in sunbeams / clean studio]

[TRANSITION CONTINUITY]:
- Start State: [Exact visual state matching prior segment terminal frame]
- Terminal State: [Exact visual pose and camera framing at segment cutoff]

[STRICT NEGATIVE PROMPTS]:
Zero turntable spin, zero 180-degree flip, zero morphing hands, zero jitter, zero watermark, zero text overlay unless explicitly scripted.
```

---

## Element Swapping & Adaptation Workflow

If the user wants to adapt the analyzed reel with changes (e.g., "Recreate this reel but featuring our brand's luxury watch" or "Replace the actor with a cyberpunk robot"):

1. **Retain the Structural Rhythm**: Keep all timecodes, cut points, camera vectors, and shot scales identical to the original reel.
2. **Inject the New Subject / Asset**: Replace the original subject in each segment's prompt with the user's asset while preserving physical kinematics.
3. **Harmonize Environment & Lighting**: Adapt the environment or keep original lighting behavior anchored to the new asset.
4. **Generate the Adapted Prompts Package**: Save as `reel_prompts_adapted.txt`.

---

## Persistent Output Directory Architecture

All reel analysis runs **must guarantee persistent file generation** under the designated directory:

```text
<project_or_reel_analysis_folder>/
├── frames/                           <-- Extracted frames (~3 per second)
│   ├── frame_0001.jpg
│   ├── frame_0002.jpg
│   └── ...
├── reel_analysis.md                  <-- Complete analytical report with tables
└── reel_prompts.txt                  <-- Ready-to-copy AI video generation prompts
```

If the user also requested adaptations/swaps:
```text
└── reel_prompts_adapted.txt          <-- Customized AI prompts with swapped elements
```
