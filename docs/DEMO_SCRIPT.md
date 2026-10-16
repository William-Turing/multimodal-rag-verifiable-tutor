# Honest two-minute research demo script

**Precondition:** Chroma DB loaded, fresh key configured, the *matching* original PDF/MP4 are available and mapped in `sources.json`. Verify these locally beforehand.

- **0:00–0:15:** Introduce the left Conversation and right Evidence Workspace. Say "This is a system and interaction prototype, not a validated learning-gain claim."
- **0:15–0:35:** Ask one genuine question about AI agents. A real retrieval call and Gemini call run.
- **0:35–0:55:** Read the answer and show retrieved evidence buttons. Explain buttons originate from Chroma node metadata, not guessed page numbers from the LLM.
- **0:55–1:15:** Select a video record with valid `seconds`; show player opening the configured media at that timestamp (only if actually verified).
- **1:15–1:40:** Select a textbook record with `page_number`; show the relevant rendered PDF page and its excerpt (only if actually verified).
- **1:40–2:00:** Explain failures are surfaced: missing/invalid mapping disables navigation, and retrieved evidence alone does not guarantee the answer is correct.

If either media file is unavailable, replace its navigation segment with an explicit limitation explanation; do not simulate playback or fabricated citations.
