"""Original PDF-figure ingestion with page provenance and key from environment."""
from __future__ import annotations
import argparse
import io
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def run(pdf_path: Path, output_dir: Path, output_json: Path):
    import fitz
    import numpy as np
    from PIL import Image
    import google.generativeai as genai

    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing GOOGLE_API_KEY")
    if not pdf_path.is_file():
        raise FileNotFoundError(pdf_path)
    genai.configure(api_key=key)
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    results = []
    with fitz.open(str(pdf_path)) as pdf:
        for page_index in range(pdf.page_count):
            page = pdf.load_page(page_index)
            for image_index, item in enumerate(page.get_images(full=True), 1):
                data = pdf.extract_image(item[0])
                with Image.open(io.BytesIO(data["image"])) as image:
                    rgb = image.convert("RGB")
                    if rgb.width < 200 or rgb.height < 200:
                        continue
                    ratio = rgb.width / rgb.height
                    if ratio < .2 or ratio > 8:
                        continue
                    arr = np.asarray(rgb.convert("L"), dtype=np.float32)
                    if arr.std() < 15 or arr.mean() < 5 or arr.mean() > 250:
                        continue
                    output_path = output_dir / f"page{page_index + 1}_img{image_index}.png"
                    rgb.save(output_path)
                    response = model.generate_content([
                        "Describe this educational figure objectively, including only clearly visible labels and relations.", rgb
                    ])
                    results.append({
                        "image_path": str(output_path),
                        "page_number": page_index + 1,
                        "description": getattr(response, "text", "") or "",
                    })
    output_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported {len(results)} image descriptions to {output_json}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--pdf", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, default=Path("Extracted_images"))
    p.add_argument("--output", type=Path, default=Path("Image_description.json"))
    x = p.parse_args()
    run(x.pdf, x.output_dir, x.output)
