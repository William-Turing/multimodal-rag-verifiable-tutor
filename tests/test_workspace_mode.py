from workspace_mode import prepare_index


def test_preview_never_invokes_backend():
    def forbidden_loader(_):
        raise AssertionError("The preview must not initialize the RAG model")
    assert prepare_index(False, forbidden_loader, "ignored") == (None, 0, None)


def test_live_uses_actual_loader():
    called_with = []
    def loader(path):
        called_with.append(path)
        return object_marker, 246
    object_marker = object()
    assert prepare_index(True, loader, "chroma_db") == (object_marker, 246, None)
    assert called_with == ["chroma_db"]


def test_loader_errors_are_surfaced_without_fake_data():
    def failed_loader(_):
        raise RuntimeError("Data unavailable")
    assert prepare_index(True, failed_loader, "unused") == (None, 0, "RuntimeError: Data unavailable")
