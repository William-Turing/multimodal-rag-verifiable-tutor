from pathlib import Path
from types import SimpleNamespace
import json
import pytest
from evidence import load_registry, make_evidence, parse_page, parse_seconds, resolve_source, label_for


def registry(tmp_path: Path, with_media: bool = True):
    (tmp_path / "assets").mkdir()
    if with_media:
        (tmp_path / "assets" / "Agents.pdf").write_bytes(b"test-pdf-magic-not-for-opening")
        (tmp_path / "assets" / "Agents.mp4").write_bytes(b"test-mp4-magic-not-for-playing")
    spec = {"sources": [
        {"id":"book", "type":"document", "path":"assets/Agents.pdf", "aliases":["PDF Document"], "display_name":"Book"},
        {"id":"lecture", "type":"video", "path":"assets/Agents.mp4", "aliases":["Video Tutorial"], "display_name":"Lecture"},
    ]}
    path = tmp_path / "sources.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    return load_registry(path, tmp_path)


def node(text, **meta):
    return SimpleNamespace(node=SimpleNamespace(metadata=meta, text=text, node_id="node-42"))


def test_validation():
    assert parse_page(32) == 32
    assert parse_page("32") == 32
    assert parse_page(-1) is None
    assert parse_page(True) is None
    assert parse_page("32.5") is None
    assert parse_seconds("287.5") == 287.5
    assert parse_seconds(0) == 0
    assert parse_seconds(float("nan")) is None
    assert parse_seconds(float("inf")) is None
    assert parse_seconds(-5) is None


def test_legacy_pdf_mapping_with_explicit_registry(tmp_path):
    r = registry(tmp_path)
    e = make_evidence(node("real indexed text", type="text", source="PDF Document", page_number=32), 0, r)
    assert (e.status, e.source_id, e.page, e.text) == ("ready", "book", 32, "real indexed text")
    assert label_for(e) == "Textbook · p.32"


def test_video_timestamp_and_label(tmp_path):
    r = registry(tmp_path)
    e = make_evidence(node("keyframe caption", type="video", source="Video Tutorial", seconds=287.1), 0, r)
    assert e.status == "ready"
    assert e.seconds == 287.1
    assert label_for(e) == "Video · 04:47"


def test_retrieval_cannot_navigate_without_mapping(tmp_path):
    e = make_evidence(node("text", type="text", source="PDF Document", page_number=32), 0, {})
    assert e.status == "unmapped"
    assert e.source_id is None


def test_asset_missing_is_explicit(tmp_path):
    e = make_evidence(node("video", type="video", source="Video Tutorial", seconds=28), 0, registry(tmp_path, with_media=False))
    assert e.status == "missing"


def test_invalid_page_time_and_image(tmp_path):
    r = registry(tmp_path)
    assert make_evidence(node("bad", type="text", source="PDF Document", page_number="??"), 0, r).status == "invalid"
    assert make_evidence(node("bad", type="video", source="Video Tutorial", seconds=-2), 0, r).status == "invalid"
    assert make_evidence(node("figure", type="image", source_id="book"), 0, r).status == "unavailable"


def test_unknown_explicit_source_id_does_not_fallback_to_alias(tmp_path):
    r = registry(tmp_path)
    e = make_evidence(node("text", type="text", source="PDF Document", source_id="mystery", page_number=2), 0, r)
    assert e.status == "unmapped"


def test_duplicate_alias_rejected(tmp_path):
    path = tmp_path / "sources.json"
    path.write_text(json.dumps({"sources": [
        {"id": "a", "type": "video", "path": "a.mp4", "aliases": ["Video Tutorial"]},
        {"id": "b", "type": "video", "path": "b.mp4", "aliases": ["Video Tutorial"]},
    ]}), encoding="utf-8")
    with pytest.raises(ValueError, match="Ambiguous"):
        load_registry(path, tmp_path)


def test_explicit_type_mismatch(tmp_path):
    r = registry(tmp_path)
    assert resolve_source({"source_id": "book"}, "video", r) is None


def test_missing_registry(tmp_path):
    assert load_registry(tmp_path / "missing.json", tmp_path) == {}
