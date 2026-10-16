"""Optional offline indexing of *your* JSON exports; never silently destroys old DB."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_nodes(pdf_file: Path, images_file: Path, video_file: Path,
               pdf_source_id: str | None = None, video_source_id: str | None = None):
    from llama_index.core.schema import TextNode

    nodes = []
    if pdf_file.is_file():
        for record in json.loads(pdf_file.read_text(encoding="utf-8")):
            meta = {"type": "text", "source": "PDF Document", "page_number": record["page"]}
            if pdf_source_id:
                meta["source_id"] = pdf_source_id
            node_kwargs = {"id_": record["node_id"]} if record.get("node_id") else {}
            nodes.append(TextNode(text=record["text"], metadata=meta, **node_kwargs))
    if images_file.is_file():
        for record in json.loads(images_file.read_text(encoding="utf-8")):
            meta = {"type": "image", "source": "PDF Figure"}
            # Do not infer page from an arbitrary filename.
            if record.get("page_number") is not None:
                meta["page_number"] = record["page_number"]
            if pdf_source_id:
                meta["source_id"] = pdf_source_id
            if record.get("image_path"):
                meta["file_path"] = str(record["image_path"])
            nodes.append(TextNode(text=record["description"], metadata=meta))
    if video_file.is_file():
        for record in json.loads(video_file.read_text(encoding="utf-8")):
            meta = {
                "type": "video", "source": "Video Tutorial",
                "timestamp": record["timestamp_str"],
                "seconds": record["timestamp_sec"],
            }
            if video_source_id:
                meta["source_id"] = video_source_id
            if record.get("frame_path"):
                meta["frame_path"] = str(record["frame_path"])
            nodes.append(TextNode(text=record["description"], metadata=meta))
    return nodes


def main():
    parser = argparse.ArgumentParser(description="Build a NEW Chroma index without overwriting the provided one")
    parser.add_argument("--pdf-json", type=Path, default=ROOT / "pdf_text.json")
    parser.add_argument("--images-json", type=Path, default=ROOT / "Image_description.json")
    parser.add_argument("--video-json", type=Path, default=ROOT / "video_data.json")
    parser.add_argument("--db-path", type=Path, default=ROOT / "chroma_db_new")
    parser.add_argument("--pdf-source-id", default=None)
    parser.add_argument("--video-source-id", default=None)
    args = parser.parse_args()

    # Validate presence and parse input *before* touching the destination.
    if not any(p.is_file() for p in (args.pdf_json, args.images_json, args.video_json)):
        parser.error("No input JSON exports exist. Index unchanged.")
    if args.db_path.exists() and any(args.db_path.iterdir()):
        parser.error(f"Destination {args.db_path} is not empty. Index unchanged; specify an EMPTY directory.")
    nodes = load_nodes(args.pdf_json, args.images_json, args.video_json, args.pdf_source_id, args.video_source_id)
    if not nodes:
        parser.error("Inputs contain no nodes. Index unchanged.")
    import chromadb
    from llama_index.core import VectorStoreIndex, StorageContext
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.vector_stores.chroma import ChromaVectorStore

    embed = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    client = chromadb.PersistentClient(path=str(args.db_path))
    collection = client.get_or_create_collection("rag_collection")
    context = StorageContext.from_defaults(vector_store=ChromaVectorStore(chroma_collection=collection))
    VectorStoreIndex(nodes, storage_context=context, embed_model=embed)
    print(f"Created {len(nodes)} records at {args.db_path}. Existing original index was not modified.")


if __name__ == "__main__":
    main()
