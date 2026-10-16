# Portfolio wording — based on implemented code, not invented outcomes

## Short project description

**Multimodal RAG Tutor — Verifiable Learning Workspace**

An evidence-first educational research prototype integrating Streamlit, Python, LlamaIndex, ChromaDB and Gemini. The design couples conversations with retrievable source records, a PDF page viewer and lecture video timestamp navigation, using explicit source metadata instead of guessing locations from generated answers. The public release provides a no-model UI Preview; the private educational dataset and Chroma index are excluded for redistribution reasons.

## Resume bullets (use only if they accurately reflect your contribution)

- Built a Python/Streamlit evidence-first interface for a multimodal retrieval-augmented educational tutor, integrating textbook-page and lecture-timestamp metadata into a split-pane inspection workflow.
- Added explicit provenance-to-viewer validation and graceful fallback states for missing or invalid source mappings while preserving the LlamaIndex/ChromaDB retrieval pipeline.
- Prepared a reproducible public code release with configuration examples, safety guards, automated unit tests and documentation, excluding third-party course media and unverified evaluation results.

## Interview answer (30 seconds)

> My project explores how learners can inspect the evidence behind an AI tutor's response. The system indexes text and visual descriptions from a PDF and lecture video, retrieves relevant evidence through ChromaDB, and uses a split-pane Streamlit workspace to let users select a retrieved source. A source registry maps stored page numbers or timestamps to local material, with explicit errors when a mapping is missing. The key research contribution is the evidence-inspection interaction, not a claim that the generated answer is automatically correct. I am keeping the full local media verification and generation reliability separate from the published UI and code status.

## Do not claim yet

Do not call it a verified end-to-end deployed service, user-study-validated tutor, hybrid BM25 retrieval engine, transcript-aligned video learner, or an automatically fact-checking system. Browser-level video seek, PDF navigation, generation availability and the revised preprint metadata need their own verification.
