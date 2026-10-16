# Feature status — 2026-10-16

| Capability | Code status | Execution verification |
| --- | --- | --- |
| Chroma persisted dense-vector retrieval | Original pipeline retained | DB SQLite quick-check passed; user observed retrieved video records in UI; no full retrieval-quality verification |
| Gemini tutoring answer | Original generation path preserved, with exception handling | Local run attempted; user saw `RetryError` during generation (root cause not yet diagnosed) |
| PDF/video/image metadata indexed | Existing 246 records in user's private DB | Static metadata inspection |
| 40:60 evidence-first Streamlit layout | UI-first visual redesign implemented | User-provided local browser screenshot confirms UI Preview layout rendering |
| UI Preview / no-model mode | Implemented; default mode bypasses index loader and never generates answers/citations | Pure Python guard unit tests pass; UI Preview visible in user-provided local screenshot |
| Retrieved-source citation buttons | Implemented for all retrieved nodes | User screenshot shows retrieved video evidence buttons and selection update; click-to-original navigation still unverified |
| Video seek | Implemented via source registry + st.video start_time | MP4 missing; actual seek untested |
| PDF page rendering and previous/next | Implemented via PyMuPDF | Matching PDF missing; browser navigation untested |
| Link generated *individual claims* to citation chip | **Not implemented** | Model may produce text references [E1] but no verified per-claim mapping |
| PDF passage highlighting | Not implemented | No bounding boxes in original metadata |
| Image original-page navigation | Not implemented for legacy records | Image page metadata missing in original index |
| Multi-source identity on legacy index | Partial explicit alias adapter | Reindex with source IDs needed for robust multiple assets |
| Streaming inference | Not implemented | Standard blocking generate_content |
| Hybrid BM25 + dense | Not implemented | Dense vector search only |
| Audio transcripts / speech-video temporal alignment | Not implemented | Frame captions only |
| Persistent user accounts and conversation history | Not implemented | Session-only state |
| Quantitative user study / benchmark claims | Not asserted | Original metrics unverified |

Static unit tests are not end-to-end verification. Never publish the old evaluation plots as validated preprint results without a separate method review.
