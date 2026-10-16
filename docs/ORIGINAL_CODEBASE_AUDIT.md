# Multimodal RAG Tutor — Phase 1 Codebase Audit

**Date:** 2026-10-15  
**Source:** User-supplied `PythonProject.zip`, reviewed offline.  
**Scope:** Static source inspection, Python AST syntax checks, read-only Chroma SQLite inspection. No API calls, no backend/server startup, no media navigation test. The revised paper PDF was not included in the received ZIP.

## 1. Technology stack (verified from source)
- **Application/UI:** Streamlit, monolithic `app.py`. `app_baseline.py` is a separate text-oriented baseline UI.
- **Retrieval and index:** ChromaDB persistent collection `rag_collection`, LlamaIndex `VectorStoreIndex` / `ChromaVectorStore`, `HuggingFaceEmbedding("BAAI/bge-small-en-v1.5")` (`app.py:34–46`, `build_index.py:85–114`).
- **LLM/VLM:** `google.generativeai`, Gemini model string `models/gemini-2.5-flash` (`app.py:26–27`, `Process_video.py:35–36`, `process_pdf_images.py:25–28`).
- **Ingestion:** PyMuPDF / `fitz` for PDF pages and embedded images; LlamaIndex `SentenceSplitter` for text chunks; OpenCV + NumPy for video-scene detection; Pillow for frame/image handling. 
- **External HTTP API:** No separate FastAPI/Flask/REST chat server implemented; Streamlit runs indexing/query/generation calls directly and sends requests to Google's generative API.
- **Dependency manifest/tests:** No `requirements.txt`, `pyproject.toml`, `.env.example`, `README.md`, or CI tests found.

## 2. Directory structure
```text
PythonProject/
  app.py                   # Main Streamlit interface + retrieve + generate
  app_baseline.py          # Baseline Streamlit interface
  process_pdf_text.py      # PDF page text -> JSON
  process_pdf_images.py    # Extract figures, VLM descriptions -> JSON
  Process_video.py         # Video scene/keyframe -> VLM JSON
  build_index.py           # JSON -> LlamaIndex/Chroma
  check_db_content.py      # Database diagnostic script
  test_search.py           # Manual retrieval trial; not automated test
  check_models.py, test_api.py
  evaluation_*.py, *_chart.py, data_comparison.py
  test_question.csv, RAG_result.csv, NoRAG_result.csv
  chart_*.png, user_study_results.png
  chroma_db/               # Chroma SQLite + vector index files
  .idea/                   # IDE-specific project files
```
**Absent:** PDF source, MP4 lecture, extracted image assets, JSON preprocessing outputs, subtitle/transcript artifacts, environment/deployment manifests.

## 3. Data flow
```
PDF (not included) ---> process_pdf_text.py --------> pdf_text.json -------+
                    \-> process_pdf_images.py ----> Image_description.json |
Video (not included) -> Process_video.py -----------> video_data.json ------+--> build_index.py
                                                                                  |
                                                                           Chroma DB
                                                                                  |
Streamlit chat input --> LlamaIndex vector retrieve, top_k=6 --> metadata + node text
        --> context string with source labels --> Gemini text generation
        --> answer in chat; original retrieved nodes shown in expanders
```
Citations inside the generated answer are **prompt-level text** rather than stable, clickable source references. UI expanders receive actual retrieved node metadata but are not linked to model answer spans. No explicit source-to-viewer resolver exists.

## 4. Existing features and status
| Feature | Status | Evidence / limitation |
|---|---|---|
| Chat question input | Implemented in code; runtime untested | `app.py:83–111` `st.chat_input`, `st.session_state` |
| Vector semantic retrieval | Implemented in code; runtime untested | `app.py:38–45,110–112`, Chroma DB data |
| LLM response generation | Implemented in code; runtime untested | `app.py:174–200` |
| Socratic/scaffolding wording | Prompt instructions only | `app.py:176–193`; no pedagogy verification |
| Textual evidence expanders | Implemented in code | `app.py:150–172` |
| Video with start-time seek | Conditional implementation in code | `app.py:153–160`: `st.video(...,start_time=int(seconds))` works only if hardcoded video file available; not linked to citation chip or persistent evidence workspace |
| Image evidence preview | Conditional implementation in code | `app.py:162–168`: relies on inaccessible absolute file paths |
| PDF page viewer/navigation | Missing | `app.py` shows only excerpt, no PDF viewer |
| Structured answer citation chips | Missing | Model writes natural-language source labels only |
| Single selected evidence panel | Missing | Evidence rendered inside the message during first generation only |
| Persistent conversation history | Missing | `st.session_state.messages` is session-local |
| Audio transcript / ASR segmentation | Not found in source | `Process_video.py` processes image frames, not audio/transcripts |
| Hybrid sparse + dense search / BM25 | Not found in retrieval pipeline | Retrieval uses embedding similarity only; Chroma internal SQLite fulltext table is **not** evidence of an application BM25 fusion pipeline |
| Resilient error handling | Partial | `init_system` catches exception but `index` may be undefined on query; generation path has no catch |

## 5. Read-only database audit
**Source:** `chroma_db/chroma.sqlite3` opened in SQLite read-only mode.
- SQLite `PRAGMA quick_check`: `ok`.
- One collection: `rag_collection`.
- **246 indexed records:** 64 `type=text`, 6 `type=image`, 176 `type=video`.
- **Text:** 64 records with `page_number`, values 1–64 (64 distinct). Page alone is not enough to identify the correct file when multiple PDFs are supported.
- **Video:** 176 records with `timestamp` + numeric float `seconds`; range approx. 0.033–1543.133 seconds. No `video_id`, media location, interval, transcript or keyframe reference in indexed video metadata.
- **Images:** 6 records with `file_path`; no `page_number` or PDF file identifier.
- **Provenance identity:** `source` values are generic labels (`PDF Document`, `PDF Figure`, `Video Tutorial`). `source_id`, stable `video_id`, `start_time`, `end_time` absent. Chroma/LlamaIndex internal `doc_id`, `document_id`, `ref_doc_id` entries evaluate as `None` and must not be confused with a stable PDF file ID.
- **Ingestion metadata loss:** `process_pdf_text.py:30–34` emits `node_id`, but `build_index.py:26–33` rebuilds TextNodes without preserving it; image filenames can encode PDF page but `build_index.py:46–53` discards that information; video JSON frame_path exists (`Process_video.py:174–181`) but `build_index.py:64–71` does not preserve it.

## 6. Risks / engineering issues ordered by priority
### P0 — Security and reproducibility
1. **Credential exposure:** At least seven Python source files contain the same literal Gemini API key: `app.py:24`, `app_baseline.py:14`, `Process_video.py:17`, `process_pdf_images.py:11`, `evaluation_RAG.py:17`, `evaluation_noRAG.py`, `check_models.py:7`. Revoke/rotate this key; remove from source; use `GOOGLE_API_KEY` from secrets/environment and a sanitized `.env.example`. Do **not** reuse leaked key.
2. **Nonportable paths and proxy:** e.g., `app.py:19–21,30–31`, `build_index.py:11–13`, `Process_video.py:13–22`. Absolute local Windows paths and forced localhost proxy break other machines.
3. **Asset absence:** no original PDF, MP4, JSON artifacts or diagram image files. Real PDF/video navigation and end-to-end retrieval + generation cannot be verified with this archive alone.
4. **Dependency manifest absent:** no pinned/capped dependency versions; the current audit environment lacks Streamlit, Chroma, LlamaIndex and the legacy `google.generativeai` package.
5. **Danger of destructive rebuild:** `build_index.py:90–95` deletes `rag_collection` before checking if JSON inputs are present. It can delete the only provided indexed dataset when executed with missing source JSON.

### P1 — Correctness, provenance and UX
6. **False ready state:** `app.py:42–54` creates or gets a collection but doesn't verify nonzero count; initialized state only indicates index object built.
7. **Unbound `index` after init error:** `app.py:49–54,110` and missing inference error handling can crash a chat turn.
8. **Uncalibrated confidence:** `app.py:122–131` maps retriever scores to `High/Med/Low` with fixed thresholds but does not establish that these represent verified answer reliability.
9. **Prompt-level citation is unstructured:** `app.py:137–148,176–196` source labels are generated as model-readable text. No validated answer-span-to-retrieval-ID mapping. Do not parse a hallucinated page/time from free text.
10. **Missing source identity:** one generic configured MP4 path and a generic PDF label are insufficient for robust multi-document/multi-video viewer mapping.
11. **UI state loss:** evidence expanders are generated inside input handling (`app.py:96–173`), while history replay (`app.py:90–93`) renders only the Markdown answer; expanders do not persist on rerun unless re-retrieved.
12. **Frame/transcript fidelity:** `Process_video.py` samples selected frames, but no speech transcript pipeline, source intervals, or cross-modal temporal alignment is implemented in supplied files.
13. **Misleading fixed UI claims:** `app.py:62–74` fixed checkboxes claim all modalities are active independent of indexed assets; footer refers to `AIED 2025` despite user-supplied 2026 context.
14. **Research materials:** `User_study_plot.py:5–10` and `data_comparison.py` include manually-entered numeric arrays; CSVs and charts alone do not establish verified experiments. Keep these outside public-facing performance claims pending provenance review, consistent with the revised preprint's scope.
15. **Copyright/privacy:** database and experiment CSVs may contain copyrighted or sensitive materials. Do not commit `chroma_db/`, source textbooks/videos, or old evaluation artifacts without clearance.

## 7. What was actually tested
- ZIP extraction with zip-slip path traversal guard: passed.
- Python `ast.parse` syntax for all 16 `.py` files: passed.
- Read-only SQLite collection/metadata audit and `quick_check`: passed.
- Streamlit UI launch: **not tested** (dependencies missing).
- Gemini API inference: **not tested** (do not use exposed credentials).
- Vector search via LlamaIndex: **not tested** (dependencies/model not installed).
- PDF navigation: **not implemented / not testable**.
- Video seek: **exists in code conditionally, not tested** (source media absent).
- Browser responsive/accessibility/console checks: **not tested**.

## 8. Recommended first implementation batch (after Phase 2 agreement)
1. **Security/configuration baseline:** Remove hardcoded credentials, conditional proxies and absolute paths; add `requirements.txt` or `pyproject.toml`, `.env.example`, `.gitignore`, startup diagnostics; preserve existing DB without deletion.
2. **Evidence adapter and in-session data contract:** Wrap actual retrieved nodes as typed evidence objects containing `evidence_id` (retrieved node ID), `type`, `content`, validated `page_number` or `seconds`, score as uncalibrated similarity, and `asset_key` from a trusted configured source registry. Missing/invalid page/time => nonclickable citation with status message. This is an adapter; no re-index required to prototype *single-asset* navigation.
3. **Streamlit 40:60 research workspace:** Conversation left; evidence panel right; separate reusable functions for evidence rendering. Keep `index.as_retriever()` and Gemini generation unchanged at first.
4. **Real clickable evidence chips and persistence:** Persist `message.evidence_ids` and retrieved evidence objects in `st.session_state`; buttons map to evidence from retrieved nodes, not free-text guesses. Display active evidence/metadata and validation state on the right.
5. **Navigation:** Video seek with configured local MP4 + validated `seconds`; PDF navigation using actual configured PDF plus page number, initially via PyMuPDF page rendering with Prev/Next, or verify a page-addressable viewer integration before claiming direct PDF.js-style navigation. No passage highlighting until offsets/coordinates exist.
6. **Smoke tests:** Pure metadata validation tests, empty-DB behavior, missing assets, invalid times/pages, and manual browser verification on real media.

## 9. What needs to be supplied for full verification
- Revised system-design preprint PDF to align implementation claims and README with paper.
- Legally shareable **matching** source PDF and lecture MP4, or local-path configuration and screenshots/video proof when source files cannot be shared.
- A fresh, **non-exposed** Gemini API key configured locally **without sending it in the chat or committing it to code**.

**Next milestone:** Agree on a minimal in-stack redesign, then patch a copy of the real project in small, tested iterations. Do not claim the current code successfully runs until an actual environment and end-to-end check passes.
