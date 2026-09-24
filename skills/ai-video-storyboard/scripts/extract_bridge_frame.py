#!/usr/bin/env python3
"""
Automated Bridge Frame Extractor (Dual-Mode: Video or Storyboard Sheet)
Part of the ai-video-storyboard skill.

Extracts the terminal frame (Frame 10) from Segment N to serve as the mandatory
starting anchor (bridge_frame.jpg) for Segment N+1.

Modes of Operation:
1. Video Mode (--video <path>):
   Extracts the final frame (at 10.00s or final frame index) from a rendered MP4 video using OpenCV.
2. Sheet Mode (--sheet <path>):
   Fallback mode when no local video file exists. Automatically crops Panel 10
   from a 4x3 Widescreen Storyboard Sheet (or Panel 5 from a 9:16 Reels Sheet 2).

Usage:
  python extract_bridge_frame.py --video path/to/segment_video.mp4 --out path/to/next_segment/bridge_frame.jpg
  python extract_bridge_frame.py --sheet path/to/storyboard_sheet.jpg --out path/to/next_segment/bridge_frame.jpg --format 16x9
"""

import os
import sys
import argparse
import cv2
import numpy as np

def extract_from_video(video_path: str, output_path: str) -> bool:
    """Extracts the final frame of an MP4 video file."""
    if not os.path.exists(video_path):
        print(f"[Error] Video file not found: {video_path}", file=sys.stderr)
        return False

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[Error] Could not open video: {video_path}", file=sys.stderr)
        return False

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    duration = total_frames / fps

    # Target the last frame (frame_count - 1)
    target_idx = max(0, total_frames - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_idx)
    ret, frame = cap.read()

    if not ret or frame is None:
        # Fallback: step backwards a few frames if the last frame was a blank container packet
        for fallback_idx in range(target_idx - 1, max(-1, target_idx - 10), -1):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fallback_idx)
            ret, frame = cap.read()
            if ret and frame is not None:
                break

    cap.release()

    if not ret or frame is None:
        print(f"[Error] Failed to read any valid frames from {video_path}", file=sys.stderr)
        return False

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, frame)
    print(f"[Success] Extracted final video frame (at {duration:.2f}s, frame #{target_idx}) to: {output_path}")
    return True

def crop_panel_from_4x3_sheet(sheet_path: str, output_path: str) -> bool:
    """
    Crops Panel 10 from a standard 4-column by 3-row Storyboard Sheet.
    In a 4x3 grid:
    - Row 1: Panels 1, 2, 3, 4
    - Row 2: Panels 5, 6, 7, 8
    - Row 3: Panels 9, 10, 11 (Slate 1), 12 (Slate 2)
    Panel 10 is at Row 2 (0-indexed), Column 1 (0-indexed).
    """
    if not os.path.exists(sheet_path):
        print(f"[Error] Storyboard sheet not found: {sheet_path}", file=sys.stderr)
        return False

    sheet = cv2.imread(sheet_path)
    if sheet is None:
        print(f"[Error] Could not load image: {sheet_path}", file=sys.stderr)
        return False

    h, w, _ = sheet.shape

    # Detect header (typically top 5% to 8% of image)
    # Estimate grid area:
    header_offset_y = int(h * 0.08)
    footer_offset_y = int(h * 0.02)
    grid_h = h - header_offset_y - footer_offset_y
    grid_w = w

    cell_h = grid_h / 3.0
    cell_w = grid_w / 4.0

    # Panel 10 is Row 2 (the 3rd row), Column 1 (the 2nd column)
    row = 2
    col = 1

    y1 = int(header_offset_y + row * cell_h + cell_h * 0.04)
    y2 = int(header_offset_y + (row + 1) * cell_h - cell_h * 0.12)  # exclude caption bar
    x1 = int(col * cell_w + cell_w * 0.03)
    x2 = int((col + 1) * cell_w - cell_w * 0.03)

    panel = sheet[y1:y2, x1:x2]
    if panel.size == 0:
        print("[Error] Calculated crop area was empty", file=sys.stderr)
        return False

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, panel)
    print(f"[Success] Cropped Panel 10 from 4x3 sheet to: {output_path}")
    return True

def crop_panel_from_reels_sheet(sheet_path: str, output_path: str) -> bool:
    """
    Crops Panel 5 from a 9:16 vertical Reels Sheet 2 (Panels 6 to 10).
    In a 5-panel vertical layout, the 5th panel (Panel 10 overall) is at the far right or bottom.
    """
    if not os.path.exists(sheet_path):
        print(f"[Error] Reels sheet not found: {sheet_path}", file=sys.stderr)
        return False

    sheet = cv2.imread(sheet_path)
    if sheet is None:
        return False

    h, w, _ = sheet.shape
    # If 5 columns side-by-side:
    panel_w = int(w / 5.0)
    panel = sheet[:, 4 * panel_w : 5 * panel_w]

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, panel)
    print(f"[Success] Cropped terminal panel from Reels sheet to: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Dual-Mode Bridge Frame Extractor")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--video", type=str, help="Path to rendered MP4 video file")
    group.add_argument("--sheet", type=str, help="Path to master storyboard sheet image")

    parser.add_argument("--out", type=str, required=True, help="Destination path for bridge_frame.jpg")
    parser.add_argument("--format", type=str, choices=["16x9", "9x16"], default="16x9", help="Target aspect ratio format")

    args = parser.parse_args()

    if args.video:
        success = extract_from_video(args.video, args.out)
    else:
        if args.format == "16x9":
            success = crop_panel_from_4x3_sheet(args.sheet, args.out)
        else:
            success = crop_panel_from_reels_sheet(args.sheet, args.out)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
