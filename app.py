"""Evidence-first research workspace. UI Preview never calls a model or retrieves evidence."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st

from evidence import label_for, load_registry, make_evidence
from rag_core import GENERATION_MODEL, load_index, retrieve, generate_answer
from source_viewer import pdf_page_count, render_pdf_page
from workspace_mode import prepare_index

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
st.set_page_config(
    page_title="Verifiable Learning | Multimodal RAG Tutor",
    page_icon="📖", layout="wide", initial_sidebar_state="collapsed"
)

EXAMPLES = [
    "What are the main components of an AI agent?",
    "How do agents decide when to use tools?",
    "What does the lecture illustrate about the agent workflow?",
]


def read_api_key() -> str:
    value = os.getenv("GOOGLE_API_KEY", "")
    if value:
        return value.strip()
    try:
        return str(st.secrets.get("GOOGLE_API_KEY", "")).strip()
    except Exception:
        return ""


@st.cache_resource(show_spinner="Opening the existing Chroma collection and BGE model…")
def cached_index(db_directory: str):
    return load_index(Path(db_directory))


@st.cache_data(show_spinner=False)
def cached_pdf_page(path: str, page_number: int) -> bytes:
    return render_pdf_page(path, page_number)


try:
    st.markdown(f"<style>{(ROOT / 'style.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
except OSError:
    pass

for key, default in {
    "messages": [], "active": None, "pdf_page": None, "preview_notice": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

try:
    registry = load_registry(ROOT / "sources.json", ROOT)
    registry_error = None
except (ValueError, KeyError, TypeError, OSError) as ex:
    registry, registry_error = {}, str(ex)

# Important: choose the UI mode BEFORE initializing the vector index. A preview launch
# never loads the Hugging Face model, never touches Gemini, and never creates citations.
starting_live = os.getenv("RAG_UI_MODE", "preview").strip().lower() == "live"
with st.sidebar:
    st.markdown('<div class="sidebar-brand">VERIFIABLE <span>LEARNING</span></div>', unsafe_allow_html=True)
    st.caption("Multimodal RAG · Research prototype")
    st.divider()
    st.markdown("#### Workspace mode")
    live_mode = st.toggle(
        "Enable Live RAG", value=starting_live,
        help="Loads the existing embedding model and Chroma index; live questions may call the Gemini API.",
    )
    if live_mode:
        st.caption("Live mode · authentic retrieval and model-generated answers")
    else:
        st.caption("UI Preview · zero retrieval, zero Gemini requests")
    st.divider()

index, record_count, init_error = prepare_index(live_mode, cached_index, str(ROOT / "chroma_db"))
api_key = read_api_key()

with st.sidebar:
    st.markdown("#### System status")
    st.write(f"**Mode:** {'Live RAG' if live_mode else 'UI Preview'}")
    st.write(f"**Index:** {'Loaded' if index is not None else ('Unavailable' if live_mode else 'Not loaded in preview')}")
    if index is not None:
        st.write(f"**Indexed records:** {record_count:,}")
    st.write(f"**Source mappings:** {len(registry)}")
    st.write(f"**Gemini key:** {'Configured locally' if api_key else 'Not configured'}")
    with st.expander("Model configuration"):
        st.caption(f"Generator: {GENERATION_MODEL}")
        st.caption("Retriever: BGE small / LlamaIndex / Chroma")
        st.caption("UI Preview skips both retrieval and generation.")
    st.divider()
    if st.button("Clear conversation", use_container_width=True, icon="🗑️"):
        st.session_state.messages = []
        st.session_state.active = None
        st.session_state.pdf_page = None
        st.session_state.preview_notice = False
        st.rerun()
    st.markdown('<div class="sidebar-note">SYSTEM & INTERACTION DESIGN<br/>No invented sources, performance claims or user-study results.</div>', unsafe_allow_html=True)

# --- App masthead ---
st.markdown(
    '<div class="masthead">'
    '<div class="masthead-top"><span class="masthead-mark">◈</span> '
    '<span class="eyebrow">MULTIMODAL LEARNING / RESEARCH INTERFACE</span></div>'
    '<div class="masthead-title">Learning, with evidence in view<span class="title-period">.</span></div>'
    '<div class="masthead-description">A conversation is the starting point — not the final authority. '
    'Trace grounded responses back to their original lecture or textbook context.</div>'
    '</div>', unsafe_allow_html=True,
)

mode_label = "UI PREVIEW · No model requests" if not live_mode else "LIVE RAG · Index enabled"
status_color = "mode-preview" if not live_mode else "mode-live"
st.markdown(
    f'<div class="status-row"><span class="mode-pill {status_color}">{mode_label}</span>'
    '<span class="status-secondary">Inspect sources, not just answers</span></div>',
    unsafe_allow_html=True,
)

steps = st.columns(3, gap="small")
for col, (number, heading, detail) in zip(steps, [
    ("01", "ASK", "Pose a course question"),
    ("02", "TRACE", "Review retrieved citations"),
    ("03", "INSPECT", "Open the original source"),
]):
    with col:
        st.markdown(
            f'<div class="workflow-step"><span class="workflow-number">{number}</span>'
            f'<span class="workflow-copy"><strong>{heading}</strong><small>{detail}</small></span></div>',
            unsafe_allow_html=True,
        )

if init_error:
    st.error(f"Knowledge base unavailable: {init_error}")
if registry_error:
    st.error(f"Source mapping configuration invalid: {registry_error}")
if live_mode and not api_key:
    st.info("No Gemini key configured. Live questions can still retrieve genuine evidence, but no generated answer will be produced.")


def choose(turn_idx: int, evidence_idx: int, item: dict) -> None:
    st.session_state.active = (turn_idx, evidence_idx)
    st.session_state.pdf_page = item.get("page")


def get_active_item() -> dict | None:
    selection = st.session_state.active
    if selection is None:
        return None
    turn_idx, evidence_idx = selection
    if not (0 <= turn_idx < len(st.session_state.messages)):
        return None
    items = st.session_state.messages[turn_idx].get("evidence", [])
    if not (0 <= evidence_idx < len(items)):
        return None
    return items[evidence_idx]


left, right = st.columns([4.4, 5.6], gap="large")

with left:
    st.markdown('<div class="pane-heading"><span class="pane-kicker">01 / DIALOGUE</span><h2>Conversation</h2><p>Ask, reflect, and follow the evidence trail.</p></div>', unsafe_allow_html=True)
    if not live_mode:
        st.markdown(
            '<div class="preview-banner"><strong>Design preview is active</strong>'
            '<span>Try the conversation controls below. Questions are displayed locally; no retrieval, '
            'AI answer, or citation is simulated.</span></div>', unsafe_allow_html=True,
        )

    if not st.session_state.messages:
        st.markdown(
            '<div class="welcome-card">'
            '<span class="welcome-tag">START HERE</span>'
            '<h3>Curiosity meets context.</h3>'
            '<p>Ask about course content. In Live RAG mode, actual indexed sources will appear '
            'beside the answer, ready for inspection.</p>'
            '</div>', unsafe_allow_html=True,
        )
        st.markdown('<div class="mini-label">SUGGESTED QUESTIONS</div>', unsafe_allow_html=True)
        for j, example in enumerate(EXAMPLES):
            if st.button(f"↗  {example}", key=f"example_{j}", use_container_width=True):
                st.session_state.pending_question = example
                st.rerun()

    for turn_idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("evidence"):
                st.caption("RETRIEVED REFERENCES · SELECT TO INSPECT")
                button_cols = st.columns(2, gap="small")
                for evidence_idx, item in enumerate(message["evidence"]):
                    active = st.session_state.active == (turn_idx, evidence_idx)
                    with button_cols[evidence_idx % 2]:
                        if st.button(
                            f"{evidence_idx + 1:02d}  {label_for(item)}",
                            key=f"evidence_{turn_idx}_{evidence_idx}",
                            type="primary" if active else "secondary",
                            use_container_width=True,
                            help=f"{item['source_name']} · {item['status']} — {item['reason']}",
                        ):
                            choose(turn_idx, evidence_idx, item)
                            st.rerun()

    if st.session_state.preview_notice and not live_mode:
        st.info("Question added locally. UI Preview does not retrieve records or generate an answer. Switch on **Enable Live RAG** in the sidebar when you want to test the actual pipeline.")

    st.markdown('<div class="composer-label">YOUR QUESTION</div>', unsafe_allow_html=True)
    pending = st.session_state.pop("pending_question", None)
    prompt = st.chat_input("Ask a question about the course…", disabled=live_mode and index is None)
    question = pending or prompt
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        if not live_mode:
            st.session_state.preview_notice = True
            st.rerun()
        if index is not None:
            with st.spinner("Retrieving indexed evidence…"):
                try:
                    nodes = retrieve(index, question)
                    evidence = [make_evidence(n, i, registry).serializable() for i, n in enumerate(nodes)]
                    if not nodes:
                        answer = "No matching indexed evidence was retrieved. I cannot provide a grounded answer."
                    elif not api_key:
                        answer = "**Retrieval-only mode:** These records are actual retrieval results. No AI answer was generated."
                    else:
                        try:
                            answer = generate_answer(api_key, question, evidence)
                        except Exception as generation_error:
                            answer = f"**Generation failed.** Retrieved evidence remains accessible. ({type(generation_error).__name__})"
                            st.error(f"Gemini error: {generation_error}")
                    st.session_state.messages.append({"role": "assistant", "content": answer, "evidence": evidence})
                    if evidence:
                        choose(len(st.session_state.messages) - 1, 0, evidence[0])
                except Exception as retrieval_error:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"**Retrieval failed.** No evidence was fabricated. ({type(retrieval_error).__name__})",
                        "evidence": [],
                    })
                    st.error(f"Search error: {retrieval_error}")
            st.rerun()
    st.markdown('<div class="below-composer">Responses require source inspection. AI text alone is not independent verification.</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="pane-heading"><span class="pane-kicker">02 / SOURCE INSPECTION</span><h2>Evidence workspace</h2><p>View provenance and inspect the original material.</p></div>', unsafe_allow_html=True)
    item = get_active_item()
    if item is None:
        st.markdown(
            '<div class="viewer-shell">'
            '<div class="viewer-toolbar"><span class="viewer-dots"><i></i><i></i><i></i></span>'
            '<strong>Source viewer</strong><span class="viewer-state">NO SOURCE SELECTED</span></div>'
            '<div class="viewer-empty"><div class="source-symbol">▤</div>'
            '<span class="viewer-pretitle">EVIDENCE INSPECTOR</span>'
            '<h3>Go beyond the generated answer.</h3>'
            '<p>When real retrieved evidence is selected, the original PDF page or video timestamp '
            'will be shown here — only if its file mapping is valid.</p></div></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="mini-label top-gap">SUPPORTED SOURCE TYPES</div>', unsafe_allow_html=True)
        a, b = st.columns(2, gap="small")
        with a:
            st.markdown(
                '<div class="source-type-card"><span class="source-type-icon">▤</span>'
                '<strong>Textbook / PDF</strong><small>Page-based inspection</small>'
                '<span class="source-type-foot">Requires mapped original PDF</span></div>',
                unsafe_allow_html=True,
            )
        with b:
            st.markdown(
                '<div class="source-type-card"><span class="source-type-icon">▷</span>'
                '<strong>Lecture / Video</strong><small>Timestamp navigation</small>'
                '<span class="source-type-foot">Requires mapped original video</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown(
            '<div class="inspection-rule"><span>VERIFICATION PRINCIPLE</span>'
            '<p>Model-generated text is not a source. Navigation is based on indexed metadata '
            'and explicitly configured files, never on guessed references.</p></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="mini-label">SELECTED RETRIEVAL RECORD</div>', unsafe_allow_html=True)
        st.markdown(f"### {label_for(item)}")
        st.caption(f"Source: {item['source_name']}  ·  Status: {item['status']}")
        if item["status"] == "ready":
            st.success("Indexed location and source file are available; actual browser navigation still requires verification.")
        else:
            st.warning(f"Navigation unavailable: {item['reason']}")

        overview_tab, metadata_tab = st.tabs(["Original source", "Provenance metadata"])
        with overview_tab:
            source = registry.get(item.get("source_id"))
            if item["status"] == "ready" and source and item["kind"] == "video":
                st.video(str(source.path), start_time=int(item["seconds"]),
                         format="video/webm" if source.path.suffix.lower() == ".webm" else "video/mp4")
                st.caption(f"Requested source timestamp: {item['seconds']:.2f} seconds. Verify the player's seek manually.")
            elif item["status"] == "ready" and source and item["kind"] in {"text", "image"}:
                try:
                    page_count = pdf_page_count(source.path)
                    current = st.session_state.pdf_page or item["page"]
                    if not (1 <= current <= page_count):
                        st.error(f"PDF page {current} is outside this file's {page_count} pages. Confirm the indexed edition.")
                    else:
                        back, counter, forward = st.columns([1, 2, 1])
                        with back:
                            if st.button("← Previous", disabled=current <= 1, use_container_width=True):
                                current -= 1
                                st.session_state.pdf_page = current
                        with counter:
                            st.markdown(f"<div class='page-indicator'>Page {current} / {page_count}</div>", unsafe_allow_html=True)
                        with forward:
                            if st.button("Next →", disabled=current >= page_count, use_container_width=True):
                                current += 1
                                st.session_state.pdf_page = current
                        st.image(cached_pdf_page(str(source.path), current),
                                 caption=f"Original file: {source.display_name} · PDF page {current}",
                                 use_container_width=True)
                except Exception as viewer_error:
                    st.error(f"Unable to open original PDF: {viewer_error}")
            elif item["kind"] == "image" and item["status"] != "ready":
                st.info("An indexed image description is available, but no verified PDF page is known.")
            else:
                st.info("The original media cannot be opened until a valid file registry and source position are configured.")
            st.markdown("#### Retrieved evidence text")
            st.write(item["text"] or "(No indexed evidence text returned)")
        with metadata_tab:
            st.json({
                "node_id": item["evidence_id"], "kind": item["kind"],
                "source_id": item["source_id"], "source_name": item["source_name"],
                "page_number": item["page"], "seconds": item["seconds"],
                "navigation_status": item["status"], "metadata": item["metadata"],
            })
        st.caption("Retrieval relevance does not prove correctness. A source file must match the indexed edition for a meaningful inspection.")

st.markdown('<div class="footer-note">VERIFIABLE LEARNING WORKSPACE <span>·</span> SYSTEM & INTERACTION DESIGN PROTOTYPE <span>·</span> EVIDENCE-FIRST</div>', unsafe_allow_html=True)
