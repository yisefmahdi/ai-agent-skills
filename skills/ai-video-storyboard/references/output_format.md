# Output Format — Folder Structure & Excel Schema

## Folder structure

Create this tree under `/mnt/user-data/outputs/<project_name>/`:

```
<project_name>/
├── storyboard.xlsx
├── Scene01_Segment01_<shortname>/
│   └── prompts.txt
├── Scene01_Segment02_<shortname>/
│   └── prompts.txt
├── Scene02_Segment03_<shortname>/
│   └── prompts.txt
└── ...
```

Rules:
- Segment numbering is **global/sequential across the whole video**, not reset per scene (Segment01, Segment02, Segment03... continuing even as Scene number increments).
- `<shortname>` is a 2-4 word slug of what happens in that segment, e.g. `Scene01_Segment01_FilmingFromHeli`, `Scene01_Segment02_TheExplosion`.
- Each segment folder is created **empty except for `prompts.txt`** — Claude does not generate the actual frame images. The empty folder is where the user will save their generated images (named `frame01.png`, `frame02.png`, etc.) after running the prompts through their chosen AI tool.
- If the user gave reference images (character/location) earlier in the conversation, copy them into a `_references/` folder at the project root and point to them by filename in the relevant VISUAL fields.

## prompts.txt format (inside each segment folder)

Plain text file, one file per segment, containing:

```
SEGMENT 01 — Scene 1: The Descent — 0:00–0:10
Aspect Ratio: 9:16
Frame count: 10

[FRAME 01 — 0:00]
VISUAL: ...
CAMERA: ...
LIGHTING: ...
MOTION/TRANSITION: ...
DIALOGUE: ...
VOICE TONE: ...
MUSIC/SFX: ...
ASPECT RATIO: 9:16
CONTINUITY: ...

[FRAME 02 — 0:01]
...
```

Use the exact field structure from `prompt_template.md` for every frame block.

## storyboard.xlsx schema

Build with the `xlsx` skill (read it before generating this file — do not hand-roll spreadsheet XML). One row per frame. Columns:

| Column | Content |
|---|---|
| Scene # | e.g. 1 |
| Scene Title | e.g. "The Descent" |
| Segment # | Global segment number, e.g. 1 |
| Segment Timerange | e.g. "0:00–0:10" |
| Frame # | e.g. 1 |
| Timestamp | e.g. "0:00" |
| Visual Summary | Short 1-line summary of the frame (not the full prompt — just enough to scan) |
| Camera | Shot type + movement, short form |
| Dialogue | The line, or blank |
| Music/SFX | Short mood/cue description |
| Folder Path | e.g. `Scene01_Segment01_FilmingFromHeli/` |
| Status | Empty column for the user to mark progress (e.g. "Not started / Generated / Approved") — leave blank, don't prefill |

Formatting notes:
- Freeze the header row.
- Auto-width columns reasonably (Visual Summary and Dialogue will be the widest).
- Group/color-code rows by Scene (alternating light fill per scene) if the xlsx skill supports easy conditional formatting — nice-to-have, not required.
- Add a second sheet named "Overview" with one row per Scene (Scene #, Title, Duration, Setting, Characters, Tone) as a quick-reference summary — optional but recommended for projects with 3+ scenes.

## Aspect ratio handling

The user specifies aspect ratio once per project (9:16, 16:9, or 1:1) — apply it to every frame's ASPECT RATIO field and note it in each `prompts.txt` header and in the Excel Overview sheet. Never mix ratios within one project unless the user explicitly asks for a format change mid-story.

## Delivery

After building the folder tree and `storyboard.xlsx`, use `present_files` to hand back the project. If there are many segment folders, presenting the top-level project folder's key files (the xlsx + maybe zip the whole tree) is preferable to listing dozens of individual `prompts.txt` paths — consider zipping the project folder with `bash_tool` (`zip -r project.zip <project_name>/`) and presenting both the zip and the xlsx separately for convenience.