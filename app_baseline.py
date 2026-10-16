"""Legacy-style text-only retrieval baseline. No evaluation results implied."""
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
from rag_core import load_index, retrieve, generate_answer
from evidence import make_evidence

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
st.set_page_config(page_title="Text-only retrieval baseline", page_icon="📄")
st.title("Text-only retrieval baseline")
st.info("This is a text-only query interface, not an experimental evaluation.")
try:
    index, count = load_index(ROOT / "chroma_db")
except Exception as e:
    st.error(f"Index not available: {e}")
    st.stop()
question = st.text_input("Question")
if st.button("Search", disabled=not question.strip()):
    try:
        # Larger dense retrieval pool, filtered by modality for the control variant.
        selected = [n for n in retrieve(index, question, top_k=20) if n.node.metadata.get("type", "text") == "text"][:3]
        ev = [make_evidence(n, i, {}).serializable() for i, n in enumerate(selected)]
        if not ev:
            st.warning("No PDF text records retrieved in the top 20.")
        else:
            key = os.getenv("GOOGLE_API_KEY", "").strip()
            if key:
                st.markdown(generate_answer(key, question, ev))
            else:
                st.info("Gemini key absent — showing retrieved text only")
            for i, e in enumerate(ev, 1):
                with st.expander(f"Text evidence {i}, page {e['page']}"):
                    st.write(e["text"])
    except Exception as ex:
        st.error(f"Query failed: {ex}")
