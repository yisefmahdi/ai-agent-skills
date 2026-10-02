#!/usr/bin/env python3
"""
Automated Bridge Frame Extractor (Dual-Mode: Video or Storyboard Sheet)
Part of the ai-video-storyboard skill (v7.0).

Extracts the terminal frame/state from Segment N to serve as the starting
anchor (bridge_frame.jpg) for Segment N+1.

Modes of Operation:
1. Video Mode (--video <path>):
   Extracts the final readable frame from a rendered MP4 video using OpenCV.
2. Sheet Mode (--sheet <path> --panel N):
   Fallback when no local video file exists. Crops panel N from a storyboard
   sheet. For a 4x3 widescreen sheet panels are 1-10 (default 10); for a
   9:16 dual-sheet workflow panels are 1-5 per sheet (default 5 = overall
   Panel 10 on sheet 2). Panel 11/12 are slate cards, never bridge frames.

Usage:
  python extract_bridge_frame.py --video path/to/segment_video.mp4 --out path/to/next_segment/bridge_frame.jpg
  python extract_bridge_frame.py --sheet path/to/storyboard_sheet.jpg --panel 10 --format 16x9 --out path/to/next_segment/bridge_frame.jpg
  python extract_bridge_frame.py --sheet path/to/reels_sheet_02.jpg --panel 5 --format 9x16 --out path/to/next_segment/bridge_frame.jpg

Dependencies: pip install -r requirements.txt
"""

import os
import sys
import argparse

try:
    import cv2
except ImportError:
    print("[Error] OpenCV (cv2) is not installed. Run: pip install -r requirements.txt",
          file=sys.stderr)
    sys.exit(2)


def extract_from_video(video_path: str, output_path: str) -> bool:
    """Extracts the final readable frame of a video file."""
    if not os.path.exists(video_path):
        print(f"[Error] Video file not found: {video_path}", file=sys.stderr)
        return False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[Error] Could not open video: {video_path}", file=sys.stderr)
        return False

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    duration = (total_frames / fps) if fps else 0.0

    target_idx = max(0, total_frames - 1)
    frame = None
    ret = False
    # Try last frame first, then step backwards (blank container packets happen).
    for fallback_idx in range(target_idx, max(-1, target_idx - 15), -1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, fallback_idx)
        ret, frame = cap.read()
        if ret and frame is not None:
            target_idx = fallback_idx
            break

    cap.release()

    if not ret or frame is None:
        print(f"[Error] Failed to read any valid frames from {video_path}", file=sys.stderr)
        return False

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, frame)
    print(f"[Success] Extracted video frame #{target_idx} (duration {duration:.2f}s) to: {output_path}")
    return True


def crop_panel_from_4x3_sheet(sheet_path: str, output_path: str, panel: int = 10) -> bool:
    """
    Crops movie panel N (1-10) from a 4-column x 3-row widescreen sheet.
    Row 3 also holds Panel 9, Panel 10, then slate cards 11-12.
    Mapping: panel 1-4 -> row 0, 5-8 -> row 1, 9-10 -> row 2 cols 0-1.
    """
    if not 1 <= panel <= 10:
        print(f"[Error] --panel must be 1-10 for 16x9 sheets (got {panel})", file=sys.stderr)
        return False
    if not os.path.exists(sheet_path):
        print(f"[Error] Storyboard sheet not found: {sheet_path}", file=sys.stderr)
        return False

    sheet = cv2.imread(sheet_path)
    if sheet is None:
        print(f"[Error] Could not load image: {sheet_path}", file=sys.stderr)
        return False

    h, w, _ = sheet.shape

    # Header/footer heuristics: top title bar ~8%, bottom margin ~2%.
    header_offset_y = int(h * 0.08)
    footer_offset_y = int(h * 0.02)
    grid_h = h - header_offset_y - footer_offset_y
    grid_w = w

    cell_h = grid_h / 3.0
    cell_w = grid_w / 4.0

    idx = panel - 1
    row = idx // 4
    col = idx % 4

    y1 = int(header_offset_y + row * cell_h + cell_h * 0.04)
    y2 = int(header_offset_y + (row + 1) * cell_h - cell_h * 0.12)  # exclude caption bar
    x1 = int(col * cell_w + cell_w * 0.03)
    x2 = int((col + 1) * cell_w - cell_w * 0.03)

    panel_img = sheet[y1:y2, x1:x2]
    if panel_img.size == 0:
        print("[Error] Calculated crop area was empty", file=sys.stderr)
        return False

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, panel_img)
    print(f"[Success] Cropped Panel {panel} from 4x3 sheet to: {output_path}")
    return True


def crop_panel_from_reels_sheet(sheet_path: str, output_path: str, panel: int = 5) -> bool:
    """
    Crops panel N (1-5) from one 9:16 vertical sheet.
    Sheet 2 panel 5 == overall Panel 10. Works for side-by-side or stacked layouts.
    """
    if not 1 <= panel <= 5:
        print(f"[Error] --panel must be 1-5 for a single 9x16 sheet (got {panel})", file=sys.stderr)
        return False
    if not os.path.exists(sheet_path):
        print(f"[Error] Reels sheet not found: {sheet_path}", file=sys.stderr)
        return False

    sheet = cv2.imread(sheet_path)
    if sheet is None:
        print(f"[Error] Could not load image: {sheet_path}", file=sys.stderr)
        return False

    h, w, _ = sheet.shape
    idx = panel - 1
    if w >= h:
        # Panels laid out horizontally side-by-side.
        panel_w = w / 5.0
        x1, x2 = int(idx * panel_w), int((idx + 1) * panel_w)
        panel_img = sheet[:, x1:x2]
    else:
        # Panels stacked vertically.
        panel_h = h / 5.0
        y1, y2 = int(idx * panel_h), int((idx + 1) * panel_h)
        panel_img = sheet[y1:y2, :]

    if panel_img.size == 0:
        print("[Error] Calculated crop area was empty", file=sys.stderr)
        return False

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, panel_img)
    print(f"[Success] Cropped panel {panel} from 9x16 sheet to: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Dual-Mode Bridge Frame Extractor (v7.0)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--video", type=str, help="Path to rendered MP4 video file")
    group.add_argument("--sheet", type=str, help="Path to master storyboard sheet image")

    parser.add_argument("--out", type=str, required=True, help="Destination path for bridge_frame.jpg")
    parser.add_argument("--format", type=str, choices=["16x9", "9x16"], default="16x9",
                        help="Storyboard sheet aspect layout (default: 16x9)")
    parser.add_argument("--panel", type=int, default=None,
                        help="Movie panel to crop in sheet mode (1-10 for 16x9, 1-5 for 9x16). Defaults: 10 / 5.")

    args = parser.parse_args()

    if args.video:
        success = extract_from_video(args.video, args.out)
    else:
        if args.format == "16x9":
            panel = args.panel if args.panel is not None else 10
            success = crop_panel_from_4x3_sheet(args.sheet, args.out, panel=panel)
        else:
            panel = args.panel if args.panel is not None else 5
            success = crop_panel_from_reels_sheet(args.sheet, args.out, panel=panel)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
