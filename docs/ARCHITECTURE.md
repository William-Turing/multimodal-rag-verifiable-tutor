# Architecture and provenance contract

## Original pipeline retained

```text
PDF -> process_pdf_text.py ---------> pdf_text.json ---+
    -> process_pdf_images.py -------> Image_description.json
MP4 -> Process_video.py ------------> video_data.json -+--> build_index.py -> ChromaDB
                                                                               |
student question -> Streamlit app.py -> LlamaIndex vector retrieve (top 6) ----+
                                                  |                  |
                                                  v                  v
                                    metadata -> evidence.py     Gemini 2.5 Flash
                                                  |                  |
                                    source registry +             answer text
                                     position check                 |
                                                  +------ UI -------+
                                                         |
                                                  evidence workspace
                                             PDF page or MP4 timestamp
```

This is a Streamlit **single-process** app. It does not expose a separate REST backend.
Its retrieval implementation is **dense semantic retrieval**, not verified hybrid BM25 + dense.
Video ingestion analyzes frames/scenes; **no speech transcription/ASR** in the supplied code.

## Trusted navigation invariants

1. Each button comes from an actual retrieved `NodeWithScore` returned by Chroma/LlamaIndex, not from a model's answer text.
2. `evidence.py:make_evidence` validates numeric `page_number` or `seconds`; missing values disable navigation.
3. `sources.json` is **user-confirmed** local mapping, not a claim that an arbitrary file matches indexed content. Legacy metadata uses `source = "PDF Document" / "Video Tutorial"` and can only map through explicitly configured aliases. For multiple PDFs/videos, re-index with stable `source_id` for each asset and use those in `sources.json`.
4. If a retrieved node has `source_id`, resolution must match that ID: no fallback to loose aliases if ID is unknown.
5. Video seek requests use `st.video` at integer seconds; only a real MP4 plus browser can prove successful playback. PDF uses PyMuPDF to rasterize a page from an actual file; page bounds are checked against the file.
6. Figure records in the provided database lack page identifiers; no guessed PDF passage or figure highlight is displayed.
7. The model is instructed to refer to `[E1]` etc., but the UI **does not yet link model claim spans to a specific evidence chip**. Chips represent retrieved context, not automatically verified support for every claim.

## Evidence shape (adapter, not index migration)

```json
{
  "evidence_id": "<retrieved node id>",
  "kind": "text | image | video",
  "text": "<actual retrieved record text>",
  "metadata": {"type": "video", "source": "Video Tutorial", "seconds": 287.1},
  "page": null,
  "seconds": 287.1,
  "source_id": "agents_lecture",
  "source_name": "Agents — Lecture",
  "status": "ready | unmapped | missing | invalid | unavailable",
  "reason": "..."
}
```

No scores are shown as confidence estimates. A similarity score is not an independently calibrated reliability metric.

## Source IDs for future multi-source indexing

Input JSON can be indexed using `--pdf-source-id` and `--video-source-id`; both persist to Chroma metadata. Until multi-source file identity exists in each record, do **not** map multiple generic `PDF Document` or `Video Tutorial` aliases to different resources.

## Accessibility and responsive behaviors

Native Streamlit buttons support keyboard activation and focus styling. Left/right columns stack on smaller screens in modern Streamlit. Video uses the browser player. The workspace uses lightweight CSS without custom JavaScript.
