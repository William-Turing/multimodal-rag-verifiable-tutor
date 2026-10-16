"""Scene-change/keyframe captions for user-owned lecture videos; NO audio ASR."""
from __future__ import annotations
import argparse
from datetime import timedelta
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def scene_difference(cv2, np, previous, current) -> float:
    before = cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)
    after = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(before, after)
    return float(np.count_nonzero(diff > 30) / diff.size)


def run(video: Path, frame_dir: Path, output: Path, min_interval: float = 2,
        max_interval: float = 60, threshold: float = 0.008):
    import cv2
    import numpy as np
    from PIL import Image
    import google.generativeai as genai

    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing GOOGLE_API_KEY")
    if not video.is_file():
        raise FileNotFoundError(video)
    genai.configure(api_key=key)
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    frame_dir.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open {video}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        cap.release()
        raise ValueError("Video FPS unavailable")
    results = []
    last_sec = -max_interval
    previous = None
    try:
        while True:
            success, frame = cap.read()
            if not success:
                break
            sec = max(0.0, (cap.get(cv2.CAP_PROP_POS_FRAMES) - 1) / fps)
            if sec - last_sec < min_interval:
                continue
            capture = previous is None or sec - last_sec >= max_interval
            if not capture:
                capture = scene_difference(cv2, np, previous, frame) > threshold
            if not capture:
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb)
            frame_path = frame_dir / f"frame_{len(results):05d}_{int(sec)}s.jpg"
            image.save(frame_path)
            result = model.generate_content([
                "Describe the educational information actually visible in this lecture frame, without assuming audio or earlier/later frames.",
                image,
            ])
            results.append({
                "timestamp_sec": sec,
                "timestamp_str": str(timedelta(seconds=int(sec))),
                "frame_path": str(frame_path),
                "description": getattr(result, "text", "") or "",
            })
            last_sec = sec
            previous = frame.copy()
            # Save incrementally for partial-work recovery.
            output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    finally:
        cap.release()
    print(f"Exported {len(results)} frame descriptions to {output}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--video", type=Path, required=True)
    p.add_argument("--frames", type=Path, default=Path("video_frames"))
    p.add_argument("--output", type=Path, default=Path("video_data.json"))
    x = p.parse_args()
    run(x.video, x.frames, x.output)
