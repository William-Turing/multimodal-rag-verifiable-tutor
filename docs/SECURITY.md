# Security and release preparation

The uploaded source ZIP had a literal Gemini API key in multiple Python scripts. **Revoke and rotate that original key** before using this project. No key is embedded in the revised code.

Before publication:

1. Use a newly issued key in local `.env` or `.streamlit/secrets.toml` and keep it private. Don't paste it in screenshots, logs, issues, notebooks, or README.
2. Start from the **copyright-safe GitHub release archive** for a clean initial GitHub repo. The **Local** ZIP deliberately includes the previously supplied Chroma DB and should *not* be uploaded as a ZIP.
3. Do not publish proprietary course material (PDF, MP4, frames, captions/indexed passages), research participant data, unreconciled experimental CSVs/charts, or the private `chroma_db` without permission. `gitignore` does not protect ZIP uploads or already-committed Git history.
4. Verify files before `git add` with `git status --short` and scan added content for keys and paths. Don't commit `.env`, `sources.json`, `assets/` media or `chroma_db/`.
5. If the original key was ever committed to a Git repo, file deletion alone does not remove it from Git history; rotate the key first and clean history before making the repository public.
6. API exceptions may contain endpoint/metadata details; avoid sharing raw full browser/terminal screenshots without review.

The local package is for development, not a public deployable hosted service. Auth/rate limiting and server isolation are not provided.
