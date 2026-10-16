# Third-party teaching materials and reproducibility

## Dataset and rights statement

The local research prototype was built using an existing textbook PDF and a lecture MP4 supplied through teaching/course sources. These files are **not original work by the application author**. Source attribution and a workshop citation **do not**, by themselves, authorize public redistribution. Rights depend on the original authors/publishers, licenses, institution policies, and applicable law; review permissions if public distribution is intended.

### Keep private / exclude from public commits and ZIP archives

- `Agents.pdf`, `Agents.mp4` and any other third-party PDF, audio or lecture media
- Screenshots, figures, keyframes and extracted page images from those materials
- `pdf_text.json`, `video_data.json`, `Image_description.json`, transcripts or captions that reproduce their substance
- `chroma_db/`, `chroma_db_new/` and any derived vector-store data: vectors and metadata may contain original text/captions, source identifiers or copies of excerpts
- `.env`, `.streamlit/secrets.toml`, local `sources.json`, secrets, absolute home paths, private account/log information

The `.gitignore` is protection for ordinary *untracked* file additions only. It does **not** remove tracked files, Git history or media deliberately placed inside a ZIP. Review all files before posting publicly.

## Safe local workflow

A local `sources.json` may point to your machine's existing PDF/video locations. It is intentionally ignored by Git. Alternatively, save locally licensed matching files in `assets/`, then copy `sources.example.json` to `sources.json` and verify identifiers, page numbers and timestamps. You do not need to publish the materials to demonstrate the implementation on your own computer.

To share a fully reproducible public demo later, create an **independent example dataset** from your own documents/video or assets explicitly licensed for redistribution; rebuild a separate public index from that dataset, keeping it clearly distinct from the private research dataset. Do not synthesize or invent retrieval results and label them as genuine.

## Honest feature statement

Public code alone supports UI Preview. It cannot reproduce the original 246-record Chroma index or show the matching lecture/page navigation without the private index and source files. UI Preview is not retrieval, and retrieved snippets are not themselves a formal validation of generated claims. Document this limitation in portfolio materials.

## Demo screenshots

Prefer screenshots of the UI Preview without third-party content. If showing retrieved content, avoid identifiable excerpts, copyrighted textbook pages and lecture frames unless the applicable rights/permissions allow publication. Do not expose credentials or local machine paths in screenshots.

This is an engineering-oriented distribution guideline, not legal advice.
