---
name: ai-video-storyboard
description: Use this skill whenever the user wants to plan, break down, or generate a storyboard/shot-list for an AI-generated video (Runway, Kling, Luma, Pika, Sora, Midjourney+animation tools, etc.), especially when they mention frame-by-frame breakdowns, "فريمات", 10-second segments, storyboard sheets (لوحات ستوري بورد مجمعة), scene breakdowns for AI video, Bridge Frames between segments, character consistency locks, microscopic director-level prompting, or persistent voice audio prompts. Trigger this any time the user describes a film/video idea (realistic, fantasy, action, sci-fi) and wants it turned into a structured production package - scenes broken into 10-second segments with 5×2 Storyboard Sheets, Bridge Frame continuity from the previous segment, strict Character & Asset DNA locking, persistent Voice DNA audio profiles, microscopic director-level cinematography prompting, and an end-of-segment physical/cinematic logic verification gate.
---

# AI Video Storyboard Generator (Microscopic Director Precision, Storyboard Sheets & Logic Gate)

## What this skill does

Turns a video idea (whether ultra-realistic docudrama, high-octane action thriller, or fantasy/sci-fi world) into a **master-level Hollywood cinematography package** ready for AI image and video generation tools (Midjourney, Runway Gen-3, Kling, Luma Dream Machine, Sora, Pika, ElevenLabs, etc.).

This skill completely eliminates AI hallucinations and visual drift through **five non-negotiable production pillars**:

1. **Master Storyboard Sheets (لوحات ستوري بورد مجمعة 5×2 أو 5+5)**:
   - Packages 10 sequential seconds into a single 5-column × 2-row contact sheet (or two 5-frame widescreen strips for intense close-ups), complete with panel numbers ①–⑩, camera directions, and action captions, saving 90% quota and giving models global scene context.
2. **Microscopic Director-Level Cinematography (صياغة مجهرية كأنك مخرج ومدير تصوير)**:
   - The AI operates as a veteran **Film Director & Director of Photography (DP)**. Prompts reject generic adjectives ("looks sad", "epic shot") and instead dictate **microscopic physical and technical facts**:
     - Exact focal lengths (e.g. 24mm wide, 35mm anamorphic, 85mm portrait prime).
     - Camera mounts & physics (Steadicam, Technocrane, 3-axis gimbal, heavy shoulder-rig inertia).
     - Optical characteristics (shallow depth of field at f/2.0, circular bokeh, anamorphic lens flare, 180-degree shutter motion blur).
     - Kinematic body mechanics (center of gravity shift, muscle tension, wind friction, momentum, weight transfer).
3. **The Bridge Frame Protocol (بروتوكول فريم الجسر الإلزامي)**:
   - Non-negotiable rule: The final frame of Segment $N$ (Frame 10) **is the exact starting anchor (Frame 01)** of Segment $N+1$.
   - The physical image is copied as `bridge_frame.jpg` into the new segment folder as the compulsory Start Frame.
4. **Strict Character & Asset DNA Lock (قفل البصمة البصرية الصارم)**:
   - Immutable positive descriptors and strict negative bans at the head of every prompt (e.g. *Strictly light-brown/tan frosted coyote fur, NEVER black; slim elongated oval face with delicate chin, NEVER round/wide*).
5. **Persistent Voice & Acoustic DNA Engine (بصمة الصوت المتطابقة والهندسة الصوتية)**:
   - Dedicated `voice_profile_prompt.txt` per segment defining the character's vocal age, timbre, resonance, shivering/breathing physics, and second-by-second lip-sync cues.
6. **The Final Logic & Physical Sanity Verification Gate (بوابة التحقق المنطقي النهائي)**:
   - At the conclusion of every segment, an explicit **4-Point Reality & Logic Audit** is performed to ensure the scene contains zero logical blunders, physics violations, or continuity jumps.

---

## Deliverables per 10-Second Segment

Each segment folder (`Scene##_Segment##_[shortname]`) contains:
1. `bridge_frame.jpg`: The reference image copied directly from the previous segment's Frame 10 (for Segment 02 and onwards).
2. `storyboard_sheet.jpg`: The generated 5×2 (or 5+5) master contact sheet.
3. `prompts.txt`: Contains:
   - `[NARRATIVE REALITY & GENRE PROFILE]` (Realism level, visual style, physics rules).
   - `[CHARACTER & ASSET DNA LOCK]` (Negative + Positive physical constraints).
   - `[BRIDGE FRAME CONTINUITY SPEC]` (Handoff link from previous segment).
   - **Part 1**: Master Storyboard Sheet Image Prompt (5×2 grid with technical captions).
   - **Part 2**: Sequential 10-Second Video Engine Prompts (Frames 01 to 10 with microscopic director specs).
   - **Part 3**: `[DIRECTOR'S LOGICAL & PHYSICAL SANITY AUDIT]` (Verification report).
4. `voice_profile_prompt.txt`: Acoustic fingerprint, emotional delivery, dialogue timing, and SFX/ambient audio mix.
5. Project-level files: `storyboard.xlsx` tracking all frames and panels, `character_location_bible.md`, and `full_script_master.txt`.

---

## Step-by-Step Production Protocol

### Step 1: Define Narrative Reality & Genre Profile
Before writing prompts, lock the foundational genre and physics laws:
- **Photorealistic / Docudrama**: Zero fantasy elements; strict Newtonian physics; naturalistic lighting; authentic weather kinetics (breath condensation in sub-zero, snow clumping on wet fabric).
- **Cinematic Action / Thriller**: Heightened reality; dynamic camera physics; practical stunt sequence framing (safety-compliant for Gemini/Runway); dramatic high-contrast lighting.
- **Sci-Fi / Fantasy**: Internal logic rules defined (e.g., zero-gravity mechanics, magical light sources, creature biology).

### Step 2: Establish the Character & Asset Bible (`character_location_bible.md`)
Lock immutable physical and acoustic traits:
- **Facial Geometry**: Bone structure, eye shape/color, chin, nose, skin tone (e.g. "Slim elongated oval face, delicate pointed chin, fair skin with cold-flushed cheeks").
- **Costume & Materials**: Exact colors, fabrics, and textures (e.g. "Matte crimson red ripstop parka, light-brown/tan frosted coyote fur hood trim — NEVER BLACK FUR").
- **Negative Invariants**: What the generator must NEVER do.
- **Vocal Signature**: Pitch, timbre, natural resonance, speech cadence, and breath sound.

### Step 3: Bridge Frame Protocol (Segment Transitions)
When transitioning from Segment $N$ to Segment $N+1$:
1. Copy Frame 10 of Segment $N$ into the new folder as `bridge_frame.jpg`.
2. Frame 01 of Segment $N+1$ MUST inherit the exact physical coordinates, posture, camera perspective, lighting, and environmental wear from Frame 10.

### Step 4: Write with Microscopic Director-Level Cinematography
Compose both the **Master Storyboard Sheet Prompt** and the **10 Sequential Video Prompts** using technical cinematic language:
- **Optics & Focal Length**: Specify 24mm, 35mm, 50mm, or 85mm. Define depth of field (shallow f/2.0 with soft background separation, or deep focus f/8).
- **Camera Rig & Motion Vector**: Steadicam tracking, slow dolly-in, handheld micro-jitter, jib crane sweep. Never change camera axes randomly mid-second unless an intentional hard cut is marked.
- **Kinematics & Weight**: Describe inertia, gravity pull, how wind deforms loose clothing, how snow yields under boot pressure.
- **Lighting Kelvin & Sources**: Cold overcast daylight (6500K–7500K), warm tungsten interior (3200K), rim lighting, catchlights in the eyes.

### Step 5: Write the Voice DNA Profile (`voice_profile_prompt.txt`)
Specify vocal fingerprint, sub-zero shivering/breathing acoustics, second-by-second dialogue timing, and audio mix ratios.

### Step 6: The Final Cinematic & Physical Logic Verification Gate
Before presenting deliverables, execute this **4-Point Logic Audit** and append the result to `prompts.txt`:
1. **Spatial & Eyeline Axis (180° Rule)**: Does the camera respect screen direction? If the character faces Screen-Right, do they remain Screen-Right unless the camera visibly tracks around them?
2. **Kinematic & Gravitational Sanity**: Are motion vectors physically sound? (e.g. If falling downward, hair and loose fabric MUST stream upward; breath vapor MUST drift with the wind).
3. **Asset & Environmental Consistency**: Do clothes, wounds, snow deposits, and props persist logically? (No miraculous healing, no suddenly dry clothes, no color shifts).
4. **Anti-Hallucination Completeness**: Is every micro-action explicitly spelled out so the generator never fills in blanks with random elements?

---

## Reference files

- `references/prompt_template.md`: Full templates for Director-Level prompts, Character DNA lock, Bridge Frame specification, Voice DNA profile, and the Logic Audit checklist.
- `references/output_format.md`: Folder layout, `prompts.txt` schema, `voice_profile_prompt.txt` format, and `storyboard.xlsx` columns.