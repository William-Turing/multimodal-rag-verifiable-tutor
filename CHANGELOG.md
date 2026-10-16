# Changes from uploaded `PythonProject.zip`

- Replaced monolithic Streamlit chat and transient evidence expanders with a split conversation / evidence workspace.
- Extracted original dense retrieval and Gemini generation integration into `rag_core.py`.
- Added `evidence.py` for type-specific validation and explicit trusted source registry mapping.
- Added PDF page raster viewer and Streamlit video timestamp viewer with missing-asset fallbacks.
- Preserved session-scoped chat/evidence selection across Streamlit reruns.
- Added loading, missing key, no index, empty retrieval, generation error, and unresolvable evidence states.
- Removed hard-coded API keys, system proxies and absolute developer-machine paths from refactored application and ingestion scripts.
- Changed destructive index replacement into safe, new-destination indexing with fail-closed input preflight.
- Preserved original `chroma_db/` in the local package without modification; excluded it from the public repository starter package.
- Added requirements, security documentation, provenance notes, feature status and tests.
- Omitted historic evaluation scripts, CSV datasets and claimed metrics from this publication-oriented version pending independent review. Original input ZIP remains untouched.

Not yet verified: real Streamlit browser behavior, model API invocation, vector retrieval runtime, real lecture playback, or PDF navigation against the missing source assets.

## UI-first redesign (2026-10-16)
- Default UI Preview that skips all BGE/Chroma initialization and does not call Gemini.
- New research-grade masthead, split-pane evidence-first workspace, explicit mode indicator, source-type cards, and improved empty/message states.
- Provenance-aware Live RAG retained; no static mock answers or fabricated citations introduced.
- New pure-function startup guard and tests; no changes to existing Chroma vectors.
