"""PDF text -> page-labelled JSON using the original SentenceSplitter strategy."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def extract_text(pdf_path: Path, output_json: Path):
    import fitz
    from llama_index.core import Document
    from llama_index.core.node_parser import SentenceSplitter

    if not pdf_path.is_file():
        raise FileNotFoundError(pdf_path)
    with fitz.open(str(pdf_path)) as pdf:
        docs = [Document(text=page.get_text(), metadata={"page": page.number + 1}) for page in pdf]
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = splitter.get_nodes_from_documents(docs)
    rows = [{"text": n.text, "page": n.metadata["page"], "node_id": n.node_id} for n in nodes]
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported {len(rows)} text segments to {output_json}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "pdf_text.json")
    args = parser.parse_args()
    extract_text(args.pdf, args.output)
