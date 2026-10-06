#!/usr/bin/env python3
"""
Reel Analyzer & Frame Extractor (v8.0)
Part of the ai-video-storyboard skill.

Extracts frames from a video reel at configurable intervals (default: 3 per second)
and generates structured analysis templates for AI video reproduction or strategic analysis.

Features:
  - Configurable capture rate (default: 3 fps = ~every 0.33s)
  - Automatic scene-cut detection using HSV histogram correlation
  - Segment grouping based on detected cuts
  - Structured analysis template (reel_analysis.md)
  - AI video reproduction prompt skeletons (reel_prompts.txt)

Usage:
  python analyze_reel.py --video path/to/reel.mp4 --out path/to/output_dir
  python analyze_reel.py --video path/to/reel.mp4 --out path/to/output_dir --fps 5
  python analyze_reel.py --video path/to/reel.mp4 --out path/to/output_dir --format 9x16

Dependencies: pip install -r requirements.txt
"""

import os
import sys
import argparse

try:
    import cv2
    import numpy as np
except ImportError:
    print("[Error] OpenCV and NumPy are required. Run: pip install -r requirements.txt",
          file=sys.stderr)
    sys.exit(2)


CUT_THRESHOLD = 0.55  # histogram correlation below this = scene cut


def format_timestamp(seconds: float) -> str:
    """Format seconds into MM:SS.mmm timestamp."""
    m = int(seconds // 60)
    s = seconds % 60
    return f"{m:02d}:{s:06.3f}"


def detect_cut(prev_frame, curr_frame, threshold: float = CUT_THRESHOLD) -> bool:
    """Detect a scene cut between two frames using HSV histogram correlation."""
    if prev_frame is None or curr_frame is None:
        return False
    prev_hsv = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2HSV)
    curr_hsv = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2HSV)
    h_bins, s_bins = 50, 60
    channels = [0, 1]
    ranges = [0, 180, 0, 256]
    prev_hist = cv2.calcHist([prev_hsv], channels, None, [h_bins, s_bins], ranges)
    curr_hist = cv2.calcHist([curr_hsv], channels, None, [h_bins, s_bins], ranges)
    cv2.normalize(prev_hist, prev_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    cv2.normalize(curr_hist, curr_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    correlation = cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_CORREL)
    return correlation < threshold


def extract_frames(video_path: str, output_dir: str, capture_fps: float = 3.0,
                   aspect_format: str = None) -> dict:
    """Extract frames at specified interval and detect scene cuts.

    Returns a dict with video metadata, extracted frame info, and cut positions.
    """
    if not os.path.exists(video_path):
        print(f"[Error] Video file not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[Error] Could not open video: {video_path}", file=sys.stderr)
        sys.exit(1)

    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / video_fps if video_fps else 0.0

    if aspect_format is None:
        aspect_format = "9x16" if height > width else "16x9"

    frame_interval = max(1, int(round(video_fps / capture_fps)))

    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[Info] Video: {video_path}")
    print(f"[Info] Resolution: {width}x{height} | FPS: {video_fps:.2f} | Duration: {duration:.2f}s")
    print(f"[Info] Aspect format: {aspect_format}")
    print(f"[Info] Capturing every {frame_interval} frames (~{capture_fps} per second)")
    print(f"[Info] Output directory: {output_dir}")
    print()

    extracted = []
    cuts = []
    prev_frame = None
    frame_idx = 0
    capture_num = 0
    segment_id = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            capture_num += 1
            timestamp = frame_idx / video_fps
            filename = f"frame_{capture_num:04d}.jpg"
            filepath = os.path.join(frames_dir, filename)
            cv2.imwrite(filepath, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])

            is_cut = detect_cut(prev_frame, frame)
            if is_cut and capture_num > 1:
                segment_id += 1
                cuts.append(capture_num)

            extracted.append({
                "num": capture_num,
                "timestamp": timestamp,
                "timestamp_str": format_timestamp(timestamp),
                "filename": filename,
                "is_cut": is_cut and capture_num > 1,
                "segment_id": segment_id,
            })

            prev_frame = frame.copy()

            if capture_num % 10 == 0:
                print(f"  Extracted frame {capture_num} at {format_timestamp(timestamp)}...")

        frame_idx += 1

    cap.release()

    print(f"\n[Info] Total frames extracted: {capture_num}")
    print(f"[Info] Scene cuts detected: {len(cuts)}")
    print(f"[Info] Segments identified: {segment_id}")

    return {
        "video_path": video_path,
        "width": width,
        "height": height,
        "video_fps": video_fps,
        "duration": duration,
        "aspect_format": aspect_format,
        "capture_fps": capture_fps,
        "total_extracted": capture_num,
        "total_segments": segment_id,
        "cuts": cuts,
        "frames": extracted,
    }


def generate_analysis_md(data: dict, output_dir: str) -> str:
    """Generate the reel_analysis.md structured analysis template."""
    filepath = os.path.join(output_dir, "reel_analysis.md")
    video_name = os.path.basename(data["video_path"])

    lines = []
    lines.append(f"# Reel Analysis Report")
    lines.append(f"## Source: `{video_name}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Video Metadata")
    lines.append("")
    lines.append("| Property | Value |")
    lines.append("| :--- | :--- |")
    lines.append(f"| **File** | `{video_name}` |")
    lines.append(f"| **Resolution** | {data['width']}×{data['height']} |")
    lines.append(f"| **Aspect Ratio** | {data['aspect_format']} |")
    lines.append(f"| **Video FPS** | {data['video_fps']:.2f} |")
    lines.append(f"| **Duration** | {data['duration']:.2f}s |")
    lines.append(f"| **Capture Rate** | {data['capture_fps']:.1f} frames/sec |")
    lines.append(f"| **Total Frames Extracted** | {data['total_extracted']} |")
    lines.append(f"| **Scene Cuts Detected** | {len(data['cuts'])} |")
    lines.append(f"| **Segments Identified** | {data['total_segments']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-frame analysis table
    lines.append("## Frame-by-Frame Analysis")
    lines.append("")
    lines.append("> Fill in the analysis columns below for each extracted frame.")
    lines.append("> Frames marked with 🔪 indicate a detected scene cut.")
    lines.append("")
    lines.append("| # | Timestamp | Seg | Cut | Image | Shot Type | Camera Move | Lighting | Subject / Action | Transition | Text / Overlay | Audio Cue | Notes |")
    lines.append("| :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    for f in data["frames"]:
        cut_mark = "🔪" if f["is_cut"] else ""
        lines.append(
            f"| {f['num']} | `{f['timestamp_str']}` | S{f['segment_id']} | {cut_mark} "
            f"| `{f['filename']}` |  |  |  |  |  |  |  |  |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")

    # Segment summary
    lines.append("## Segment Summary")
    lines.append("")
    lines.append("| Segment | Start Time | End Time | Duration | Frames | Description | Camera Pattern | Lighting | Mood / Energy |")
    lines.append("| :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- |")

    # Group frames by segment
    segments = {}
    for f in data["frames"]:
        sid = f["segment_id"]
        if sid not in segments:
            segments[sid] = []
        segments[sid].append(f)

    for sid in sorted(segments.keys()):
        seg_frames = segments[sid]
        start_t = seg_frames[0]["timestamp_str"]
        end_t = seg_frames[-1]["timestamp_str"]
        dur = seg_frames[-1]["timestamp"] - seg_frames[0]["timestamp"]
        lines.append(
            f"| S{sid} | `{start_t}` | `{end_t}` | {dur:.2f}s | {len(seg_frames)} |  |  |  |  |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")

    # Analysis sections
    sections = [
        ("Overall Analysis Summary",
         "Summarize the reel's visual strategy, storytelling approach, pacing, and production quality."),
        ("Shot Sequence Map",
         "Map the progression of shots: how they build narrative or emotional momentum.\n>\n> ```\n> S1 (Wide Establishing) → S2 (Medium Action) → S3 (Close-up Emotion) → ...\n> ```"),
        ("Camera Movement Pattern",
         "Document the camera movement vocabulary used: static, pan, tilt, dolly, crane, handheld, drone, etc."),
        ("Color Grading & Lighting Analysis",
         "Describe the color palette, Kelvin temperature shifts, contrast style, and volumetric lighting usage."),
        ("Pacing & Rhythm Analysis",
         "Analyze cut frequency, beat timing, acceleration/deceleration patterns, and hooks."),
        ("Text, Graphics & Overlay Analysis",
         "List all on-screen text, motion graphics, lower thirds, subtitles, logos, and their timing."),
        ("Audio & Music Sync Notes",
         "Describe music beats, sound effects, voiceover timing, and how audio syncs with visual cuts."),
        ("Continuity & Transition Notes",
         "Document transition types (hard cut, dissolve, wipe, zoom, etc.) and continuity between segments."),
    ]

    for title, desc in sections:
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"> {desc}")
        lines.append("")
        lines.append("*(Fill in your analysis here)*")
        lines.append("")
        lines.append("---")
        lines.append("")

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"[Success] Analysis template saved to: {filepath}")
    return filepath


def generate_prompts_file(data: dict, output_dir: str) -> str:
    """Generate reel_prompts.txt with AI video prompt skeletons per segment."""
    filepath = os.path.join(output_dir, "reel_prompts.txt")
    video_name = os.path.basename(data["video_path"])

    lines = []
    lines.append("=" * 80)
    lines.append("REEL ANALYSIS — AI VIDEO REPRODUCTION PROMPTS (v8.0)")
    lines.append(f"Source: {video_name}")
    lines.append(f"Resolution: {data['width']}×{data['height']} | Aspect: {data['aspect_format']}")
    lines.append(f"Duration: {data['duration']:.2f}s | Segments: {data['total_segments']}")
    lines.append("=" * 80)
    lines.append("")

    # Group frames by segment
    segments = {}
    for f in data["frames"]:
        sid = f["segment_id"]
        if sid not in segments:
            segments[sid] = []
        segments[sid].append(f)

    for sid in sorted(segments.keys()):
        seg_frames = segments[sid]
        start_t = seg_frames[0]["timestamp_str"]
        end_t = seg_frames[-1]["timestamp_str"]
        dur = seg_frames[-1]["timestamp"] - seg_frames[0]["timestamp"]
        ref_frames = ", ".join(f["filename"] for f in seg_frames[:3])

        lines.append("-" * 80)
        lines.append(f"SEGMENT S{sid} [{start_t} – {end_t}] (Duration: {dur:.2f}s)")
        lines.append(f"Reference Frames: {ref_frames}")
        lines.append("-" * 80)
        lines.append("")
        lines.append("[VISUAL DESCRIPTION]:")
        lines.append("(Describe the scene: subjects, environment, composition, colors, textures)")
        lines.append("")
        lines.append("[CAMERA]:")
        lines.append("(Shot type, lens, movement, angle)")
        lines.append("")
        lines.append("[LIGHTING & COLOR]:")
        lines.append("(Kelvin temperature, direction, quality, color grading, volumetric effects)")
        lines.append("")
        lines.append("[MOTION & ACTION]:")
        lines.append("(Subject movement, speed, direction, interaction, gesture)")
        lines.append("")
        lines.append("[TRANSITION IN]:")
        lines.append("(How this segment starts: cut from previous, dissolve, wipe, match-cut, etc.)")
        lines.append("")
        lines.append("[TRANSITION OUT]:")
        lines.append("(How this segment ends / connects to the next segment)")
        lines.append("")
        lines.append("[TEXT / OVERLAY]:")
        lines.append("(Any on-screen text, graphics, subtitles, logos)")
        lines.append("")
        lines.append("[AUDIO]:")
        lines.append("(Music beat, SFX, voiceover, dialogue, ambient sound)")
        lines.append("")
        lines.append("[AI VIDEO PROMPT]:")
        lines.append("(Write the complete AI video generation prompt for this segment here)")
        lines.append("")
        lines.append("")

    lines.append("=" * 80)
    lines.append("END OF REEL ANALYSIS PROMPTS")
    lines.append("=" * 80)

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"[Success] Prompts template saved to: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Reel Analyzer & Frame Extractor (v8.0) — ai-video-storyboard skill"
    )
    parser.add_argument("--video", type=str, required=True,
                        help="Path to the video reel file (MP4, MOV, etc.)")
    parser.add_argument("--out", type=str, default=".",
                        help="Output directory for frames and analysis files (default: current dir)")
    parser.add_argument("--fps", type=float, default=3.0,
                        help="Capture rate in frames per second (default: 3.0 = ~every 0.33s)")
    parser.add_argument("--format", type=str, choices=["16x9", "9x16"], default=None,
                        help="Force aspect format (default: auto-detect from video dimensions)")

    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    data = extract_frames(args.video, args.out, capture_fps=args.fps, aspect_format=args.format)
    generate_analysis_md(data, args.out)
    generate_prompts_file(data, args.out)

    print(f"\n[Done] Reel analysis complete.")
    print(f"  Frames: {os.path.join(args.out, 'frames')}")
    print(f"  Analysis: {os.path.join(args.out, 'reel_analysis.md')}")
    print(f"  Prompts: {os.path.join(args.out, 'reel_prompts.txt')}")


if __name__ == "__main__":
    main()
