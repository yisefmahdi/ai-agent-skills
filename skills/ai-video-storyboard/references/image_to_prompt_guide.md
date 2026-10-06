# IMAGE-TO-PROMPT — Ultra-Detailed Image Reverse Engineering Guide (v8.0)

> This guide is the detailed reference for the **IMAGE-TO-PROMPT** mode of the `ai-video-storyboard` skill. It defines the analysis protocol, the element swap/edit workflow, and provides prompt templates for converting any image into a high-fidelity AI generation prompt.

---

## Purpose

Convert any supplied image into an exhaustive, production-grade AI image-generation prompt that captures **every reproducible visual property** of the source. The resulting prompt can be used with any AI image generator (Midjourney, DALL-E, Stable Diffusion, Gemini Imagen, Ideogram, Flux, etc.) to reproduce or adapt the original image.

---

## Analysis Protocol — The 12 Mandatory Dimensions

When analyzing an image, **all 12 dimensions must be covered** in the output prompt. Skip a dimension only if it is genuinely not applicable (e.g., no text in the image → skip Typography).

### 1. Exact Dimensions & Aspect Ratio
- Detect pixel dimensions (e.g., 1920×1080)
- State aspect ratio: 16:9, 9:16, 1:1, 4:5, 3:4, 4:3, 3:2, 2:3, 21:9, etc.
- State orientation: landscape, portrait, or square
- Note if the image appears cropped or has non-standard margins

### 2. Visual Medium & Rendering Style
Identify the primary visual medium and any sub-styles:
- **Photography**: editorial, fashion, product, street, portrait, landscape, macro, aerial, underwater, documentary
- **Digital Art**: concept art, matte painting, digital illustration, vector
- **3D Render**: hyper-realistic CGI, Pixar/Disney style, Unreal Engine, Blender, low-poly
- **Traditional Art**: oil painting, watercolor, pencil sketch, charcoal, ink, pastel
- **Mixed/Special**: collage, double exposure, cinemagraph, pixel art, anime/manga, retro poster

### 3. Camera & Lens Properties (Photographic Images)
- **Focal length estimate**: ultra-wide (<24mm), wide (24-35mm), normal (35-50mm), portrait (50-85mm), telephoto (85-200mm), super-tele (>200mm), macro
- **Depth of field**: deep (everything sharp), shallow (subject sharp, background blurred), ultra-shallow (razor-thin focal plane)
- **Bokeh quality**: circular, hexagonal, anamorphic oval, swirly, smooth creamy
- **Lens effects**: distortion (barrel/pincushion), chromatic aberration, lens flare, vignette
- **Motion**: frozen action, motion blur (subject or background), long exposure trails
- **Film stock / sensor**: clean digital, film grain (fine/coarse), noise pattern

### 4. Composition & Framing
- **Rule**: thirds, centered, symmetrical, golden ratio, fibonacci spiral, diagonal
- **Subject position**: center, left/right third, upper/lower portion, quadrant (TL, TR, BL, BR)
- **Horizon**: high, middle, low, tilted (Dutch angle)
- **Leading lines**: convergent, diagonal, curved, architectural
- **Negative space**: amount and placement (left, right, above, below)
- **Framing devices**: natural frames (doorways, windows, branches), vignette framing
- **Layering**: foreground interest, midground subject, background depth

### 5. Lighting Analysis
- **Key light**: direction (front, 45° side, 90° side, rim/back, top, bottom, Rembrandt, butterfly, split)
- **Quality**: hard (sharp shadows) vs. soft (diffused, gradual transitions)
- **Fill light**: ratio to key (1:1 flat, 2:1 subtle, 4:1 dramatic, 8:1 extreme)
- **Accent/rim lights**: presence, direction, color
- **Color temperature**: warm (<3500K), neutral (4000-5500K), cool (>6000K), mixed
- **Volumetric effects**: god rays, fog/haze scatter, dust particles, underwater caustics
- **Practical lights**: visible light sources in frame (lamps, screens, fire, neon, candles)
- **Shadows**: hard-edged, soft-edged, colored, ambient occlusion

### 6. Color Palette & Grading
- **Dominant colors**: list 3-5 primary colors with approximate hex codes
- **Color harmony**: complementary, analogous, triadic, split-complementary, monochromatic
- **Saturation**: desaturated/muted, natural, vivid/hyper-saturated
- **Contrast**: low (flat), medium (natural), high (punchy), extreme
- **Tonal range**: high-key (bright, airy), low-key (dark, moody), full-range, mid-tone
- **Color grading style**: teal-orange, cross-processed, bleach bypass, vintage film emulation (Kodak Portra, Fuji Velvia), matte/flat, cinematic LUT, pastel, neon

### 7. Subject Description
For **each subject** in the image, provide an exhaustive description:
- **People**: estimated age, gender, ethnicity/skin tone, facial features (face shape, eyes, nose, mouth, jawline), expression (specific emotion + intensity), body pose (stance, hand position, weight distribution), gaze direction (to camera, away, down, up), hair (color, length, style, texture), skin texture (smooth, freckled, weathered, oily)
- **Animals**: species, breed, color, fur/feather texture, posture, expression
- **Objects**: material, texture, color, condition (new/worn/aged), scale relative to frame
- **Text content**: exact wording, language

### 8. Wardrobe & Styling (For People)
- **Each garment**: type, material (cotton, silk, leather, denim, wool), color, pattern (solid, striped, plaid, floral), fit (tight, loose, oversized, tailored), condition
- **Accessories**: jewelry (type, material, style), watches, glasses/sunglasses, bags, hats, scarves, belts
- **Footwear**: type, color, material, condition
- **Makeup**: foundation level, eye makeup style, lip color, contouring, special effects makeup
- **Hair styling**: product, volume, direction, accessories (clips, bands, ribbons)

### 9. Environment & Background
- **Setting type**: indoor (room type), outdoor (landscape type), studio (backdrop color/type)
- **Architecture**: style, materials, scale, condition
- **Nature**: vegetation type, terrain, sky condition, water features
- **Floor/surface**: material, texture, reflectivity
- **Depth layers**: foreground elements, midground features, background vista
- **Atmospheric effects**: fog/haze (density), rain, snow, dust, smoke, fire, sparks
- **Time of day**: golden hour, blue hour, midday, sunset, night, overcast

### 10. Text & Typography (If Present)
- **Exact text content**: word-for-word transcription
- **Font classification**: serif, sans-serif, script/cursive, display/decorative, handwritten, monospace
- **Weight**: light, regular, bold, black, ultra-bold
- **Size**: relative to frame (small accent, medium body, large headline, full-frame)
- **Color**: text color, outline/stroke color, shadow color
- **Position**: top, center, bottom, left-aligned, right-aligned, overlaid on subject
- **Effects**: drop shadow, outer glow, 3D extrusion, outline/stroke, gradient fill, texture fill, distortion/warp

### 11. Mood & Atmosphere
- **Emotional tone**: joyful, melancholic, tense, serene, powerful, mysterious, romantic, eerie, energetic, nostalgic
- **Energy level**: calm/still, moderate, dynamic, explosive
- **Narrative implication**: what story does this image suggest?
- **Cinematic genre feel**: action, drama, horror, romance, sci-fi, fantasy, documentary, noir, comedy

### 12. Post-Processing & Effects
- **Vignette**: presence, intensity, color
- **Grain/noise**: fine film grain, coarse grain, digital noise, clean
- **Blur effects**: gaussian, radial, tilt-shift, bokeh overlay
- **Color effects**: split toning, duotone, selective color
- **Overlay textures**: light leaks, scratches, paper texture, halftone
- **Special effects**: glitch, double exposure, kaleidoscope, long exposure, HDR merge

---

## Element Swap / Edit Protocol

When the user wants to replace or modify a specific element:

### Step 1: Lock Unchanged Properties
Copy all 12 dimensions from the original analysis. Mark the element being changed with `[SWAP TARGET]`.

### Step 2: Describe Replacement
Write the new element with **equal or greater detail** than the original. Match:
- Same position in frame (quadrant, scale, overlap with other elements)
- Same lighting interaction (shadow direction, highlight placement, rim light)
- Same color grading (the replacement must feel native to the palette)
- Same depth of field behavior (sharp if original was sharp, blurred if it was in the bokeh zone)

### Step 3: Output Both Prompts
1. **ORIGINAL PROMPT**: Faithful reproduction of the source image
2. **MODIFIED PROMPT**: Same as original but with the swap applied

### Step 4: Continuity Check
Verify that the swap doesn't break:
- Spatial logic (a tall subject replacing a short one may need composition adjustment)
- Lighting physics (a reflective surface replacing a matte one changes specular behavior)
- Color harmony (a bright red subject in a teal-graded image may need grading notes)

---

## Output Format

### On-Screen Display
Always show the full prompt in a clean, copy-ready code block:

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

### File Save
- If a project directory is active, save to `<project_dir>/image_prompt_<YYYYMMDD_HHMMSS>.txt`
- If no project directory, present as copyable text only
- Always inform the user whether the file was saved and where

---

## Quick Examples

### Example 1: Simple reproduction
User: "Here's a photo. Give me a prompt to recreate it."
→ Analyze all 12 dimensions → Output the complete prompt

### Example 2: Person swap
User: "Same photo but replace the woman with an elderly man reading a newspaper."
→ Analyze all 12 dimensions → Lock everything except Subject 1 → Describe the elderly man with matching lighting/position/scale → Output ORIGINAL + MODIFIED prompts

### Example 3: Text change
User: "Change the sign text from 'OPEN' to 'WELCOME HOME'."
→ Analyze all 12 dimensions → Lock everything except Text → Match font style, size, color, effects → Output ORIGINAL + MODIFIED prompts

### Example 4: Background swap
User: "Same person but put them on a beach at sunset."
→ Analyze all 12 dimensions → Lock subject, wardrobe, pose → Replace environment → Adjust lighting to match sunset (warm 3200K, golden hour direction) → Output ORIGINAL + MODIFIED prompts
