# Frame Prompt Template & Worked Example

## The exact field structure (use for every single frame, no exceptions)

```
[FRAME 0X — 0:0X]
VISUAL: <full scene description: who/what is in frame, exact action happening, setting details, composition/framing>
CAMERA: <shot type (wide/medium/close-up/extreme close-up), angle (eye-level/low/high/dutch), and movement (static/pan/tilt/dolly/handheld) with direction + speed>
LIGHTING: <light source, direction, color temperature (warm/cool/neutral, or Kelvin if useful), mood it creates>
MOTION/TRANSITION: <exactly how this frame moves or cuts into the next — e.g. "character's head turns 15° left over the next second, snow continues falling at same rate">
DIALOGUE: <exact line in requested language, or "None">
VOICE TONE: <delivery direction if dialogue present — pace, emotion, breathiness, volume — or "N/A">
MUSIC/SFX: <what's playing or what sound effect triggers here, and its mood/intensity>
ASPECT RATIO: <e.g. 9:16>
CONTINUITY: <what must visually match frame before this one — character pose/expression carryover, lighting consistency, prop positions>
```

## Why every field matters (don't skip fields to save time)

- **Repeating ASPECT RATIO and core visual anchors on every frame** is deliberate, not redundant — most AI generators process each prompt independently with no memory of prior frames. If you rely on "it'll remember from frame 1," you'll get hallucinated inconsistencies (wrong hair color, different jacket, camera ratio drift). Treat every frame prompt as if it's the generator's *only* piece of context.
- **CONTINUITY is the actual anti-hallucination mechanism.** It's not decorative — it's the explicit bridge that stops the model from reinventing the character or scene each frame.
- **One beat of change per frame.** If you pack two seconds of action into one frame's MOTION field, the generator has to guess the in-between — that's exactly the hallucination source this whole system exists to avoid.

## Worked example — Segment 1 (0:00–0:10), "Scene 1: The Descent"

Context this example assumes (for calibration only — always replace with the real project's story): a girl is filming through a helicopter window over Antarctic ice; the helicopter has just been hit and is going down. Aspect ratio 9:16. Dialogue in Arabic, visual prompts in English.

```
[FRAME 01 — 0:00]
VISUAL: Young woman, early 20s, wearing a red insulated parka and fogged ski goggles pushed up on her forehead, sits by the open side door of a helicopter, handheld camera raised to her eye, filming the white Antarctic ice sheet below through the door gap. Helicopter interior visible: gray metal frame, a safety strap across her chest, small vibration blur on loose gear.
CAMERA: Medium shot, slight low angle from inside the cabin looking toward her, static.
LIGHTING: Bright flat overcast daylight, cool color temperature (~7000K), diffused through cloud cover, minimal shadow.
MOTION/TRANSITION: Helicopter vibrates subtly; her camera hand adjusts focus slightly forward over the next second.
DIALOGUE: "هاي، هلق عم نطير فوق القطب الجنوبي!" (excited, to her own camera)
VOICE TONE: Bright, energetic, slightly raised to be heard over rotor noise.
MUSIC/SFX: Helicopter rotor thrum (steady, mid-volume), wind whistle through open door.
ASPECT RATIO: 9:16
CONTINUITY: Opening frame — establishes baseline: red parka, goggles up, handheld camera, cabin framing. All following frames in this segment must preserve these exact details unless the prompt explicitly changes them.

[FRAME 02 — 0:01]
VISUAL: Same woman, same framing, now a sudden orange-white flash and puff of smoke erupts from the helicopter's tail section, visible through the open door behind her. Her expression shifts to shock, eyes widening, camera hand freezing mid-motion.
CAMERA: Same medium shot, static, no movement — the stillness sells the shock beat.
LIGHTING: Same flat overcast daylight; brief warm flash-light spill from the explosion reflects on the cabin's metal interior for this frame only.
MOTION/TRANSITION: The explosion flash expands slightly frame-to-frame; helicopter begins a subtle tilt to the right, felt rather than seen yet.
DIALOGUE: None
VOICE TONE: N/A
MUSIC/SFX: Sharp explosion bang, rotor thrum distorts/stutters, wind noise sharpens.
ASPECT RATIO: 9:16
CONTINUITY: Same red parka, same goggles-up position, same handheld camera grip as Frame 01. Only new element: explosion flash + shocked expression.

[FRAME 03 — 0:02]
VISUAL: Helicopter cabin now visibly tilted ~20° to the right, loose gear sliding across the floor toward the open door. Woman grips the door frame with her free hand, camera still in her other hand but pointed downward now, unintentionally still recording.
CAMERA: Medium shot becomes canted/dutch angle matching the helicopter's tilt, slight handheld shake introduced.
LIGHTING: Same cool overcast light, now with fast-moving shadow flicker from the tilting airframe.
MOTION/TRANSITION: Tilt continues increasing toward next frame; a warning light begins flashing red in the background.
DIALOGUE: "!Oh my God" — reflexive English exclamation (adjust to Arabic if the user prefers full-Arabic dialogue: "يا الله!")
VOICE TONE: Panicked, breathless, involuntary.
MUSIC/SFX: Rising alarm tone inside cabin, wind roar intensifying, rotor stutter continues.
ASPECT RATIO: 9:16
CONTINUITY: Same character design as Frames 01-02. Tilt increases from implied/felt (Frame 02) to visually explicit (Frame 03) — this is the one new beat this frame adds.

[... Frames 04–10 continue the same way: one clear beat of change per frame, explicit continuity notes, until segment ends at 0:10 — e.g. Frame 10 could end on the door blowing open / her beginning to fall, setting up Segment 2.]
```

## Notes on adapting this template

- If the user's segment has **fast action** (crashes, fights, quick cuts), increase frame count above 10 for that segment and say so explicitly to the user — e.g. "used 14 frames for this segment because of the explosion beat."
- If a segment is **calm/dialogue-heavy**, 10 frames (1/sec) is usually sufficient — don't over-fragment slow scenes.
- If the user has **character/location reference images**, add a line to VISUAL noting which reference to use, e.g. `VISUAL: [Use reference: Girl_Character.png for face/outfit consistency] + ...`
- Keep VISUAL descriptions self-contained — never write "same as before" without restating the actual details, since the generator won't have "before" in context.