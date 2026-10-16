import subprocess
import sys
from pathlib import Path


def test_no_json_never_creates_index(tmp_path):
    build = Path(__file__).resolve().parents[1] / "build_index.py"
    db = tmp_path / "should-not-be-created"
    run = subprocess.run([
        sys.executable, str(build),
        "--pdf-json", str(tmp_path / "missing_a.json"),
        "--images-json", str(tmp_path / "missing_b.json"),
        "--video-json", str(tmp_path / "missing_c.json"),
        "--db-path", str(db),
    ], capture_output=True, text=True)
    assert run.returncode != 0
    assert not db.exists()


def test_nonempty_existing_index_never_overwritten(tmp_path):
    build = Path(__file__).resolve().parents[1] / "build_index.py"
    db = tmp_path / "old_db"
    db.mkdir()
    sentinel = db / "sentinel.data"
    sentinel.write_text("do-not-delete")
    data = tmp_path / "pdf.json"
    data.write_text('[{"page":1,"text":"real"}]')
    run = subprocess.run([
        sys.executable, str(build),
        "--pdf-json", str(data),
        "--images-json", str(tmp_path / "missing.json"),
        "--video-json", str(tmp_path / "missing2.json"),
        "--db-path", str(db),
    ], capture_output=True, text=True)
    assert run.returncode != 0
    assert sentinel.read_text() == "do-not-delete"
