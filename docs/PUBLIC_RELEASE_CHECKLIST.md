# Public GitHub release checklist

**Before the first public commit**

- [ ] Use a fresh repository containing only the **GitHub Safe** package contents, not your whole working directory or local ZIP.
- [ ] Verify `assets/` contains only `.gitkeep` (no PDF, MP4, frames, images or source extracts).
- [ ] Verify `chroma_db/`, `chroma_db_new/`, `.env`, `sources.json`, local logs/exports and `.venv/` are absent.
- [ ] Verify no API keys, account information, local desktop paths or experiment/user-study results in files or screenshots.
- [ ] Keep `sources.example.json` with project-relative paths and source aliases; no working private absolute path is necessary for public checkout.
- [ ] Check README's stated feature status. Default UI Preview is a visual/interaction preview, not real RAG inference.
- [ ] Decide whether you own rights to release the code under a selected license; don't license third-party materials as though they were yours.
- [ ] Only include paper citation metadata that has been verified against the revised preprint and workshop program.

**Windows PowerShell (inside a NEW folder created from the GitHub Safe ZIP):**

```powershell
git init
git add .
git status --short
# Verify the staged file list manually before making the first commit.
git diff --cached --name-only
```

If any private materials are staged, remove them **before committing**. A `.gitignore` does not remove files already tracked. If the repository was previously public with a key committed to history, replace/rotate that key and handle repository history separately.

**After review:**

```powershell
git commit -m "Initial public research prototype"
```

You can then create an empty repository on GitHub and follow its provided `git remote add` and `git push` commands. GitHub code upload and copyright permissions are distinct: a private copy is not permission to re-upload course media.
