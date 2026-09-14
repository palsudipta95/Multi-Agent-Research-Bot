import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(page_title="ResearchMind", page_icon="🧠", layout="wide")
 
# ---------------------------------------------------------------------------
# STYLES
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg: #0a0a0c;
    --panel: #141417;
    --panel-border: #232327;
    --orange: #ff7a2f;
    --text: #f2f1ee;
    --muted: #8a8a92;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: var(--bg); color: var(--text); }
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 3rem; max-width: 1180px; }

/* Hero */
.eyebrow {
    text-align: center;
    color: var(--orange);
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    font-weight: 600;
    font-family: 'Space Grotesk', sans-serif;
    margin-bottom: 0.6rem;
}
.hero-title {
    text-align: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 4.2rem;
    line-height: 1;
    letter-spacing: -0.02em;
    margin: 0 0 1.1rem 0;
}
.hero-title .a { color: var(--text); }
.hero-title .b { color: var(--orange); }
.hero-sub {
    text-align: center;
    color: var(--muted);
    font-size: 1.02rem;
    line-height: 1.55;
    max-width: 560px;
    margin: 0 auto 3rem auto;
}

/* Section label */
.section-label {
    color: var(--orange);
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    font-weight: 600;
    font-family: 'Space Grotesk', sans-serif;
    margin-bottom: 0.5rem;
}
.panel-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.45rem;
    margin-bottom: 1.1rem;
    color: var(--text);
}

/* Input */
.stTextInput input {
    background: var(--panel) !important;
    border: 1px solid var(--panel-border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    padding: 0.85rem 1rem !important;
    font-size: 0.95rem !important;
}
.stTextInput input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 1px var(--orange) !important;
}
.stTextInput input::placeholder { color: #55555c !important; }

/* Button */
.stButton button {
    width: 100%;
    background: linear-gradient(135deg, var(--orange), #ff5f1f) !important;
    color: #160a00 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 1rem !important;
    font-weight: 700 !important;
    font-size: 0.98rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    box-shadow: 0 8px 24px -8px rgba(255,122,47,0.55);
    transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 28px -6px rgba(255,122,47,0.7);
}
.stButton button:disabled {
    background: #26262a !important;
    color: #55555c !important;
    box-shadow: none;
}

/* Try chips */
.try-label {
    color: var(--muted);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    font-weight: 600;
    margin: 1.6rem 0 0.7rem 0;
}

/* Pipeline cards */
.pipe-card {
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.85rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    transition: border-color 0.2s ease, background 0.2s ease;
}
.pipe-card.active { border-color: var(--orange); background: #1c140c; }
.pipe-card.done { border-color: #2c4a34; }
.pipe-left { display: flex; gap: 0.8rem; }
.pipe-num {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--muted);
    font-size: 0.78rem;
    font-weight: 600;
    padding-top: 0.15rem;
}
.pipe-card.active .pipe-num { color: var(--orange); }
.pipe-card.done .pipe-num { color: #4caf6f; }
.pipe-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text);
    margin-bottom: 0.2rem;
}
.pipe-desc { color: var(--muted); font-size: 0.8rem; }
.pipe-status {
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    font-weight: 600;
    color: #55555c;
    padding-top: 0.2rem;
    white-space: nowrap;
}
.pipe-card.active .pipe-status { color: var(--orange); }
.pipe-card.done .pipe-status { color: #4caf6f; }

/* Result cards */
.result-card {
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}
.result-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 0.8rem;
    color: var(--text);
}
.result-body {
    color: #cfcfd4;
    font-size: 0.9rem;
    line-height: 1.65;
    white-space: pre-wrap;
}

/* Footer */
.footer {
    text-align: center;
    color: #4a4a50;
    font-size: 0.78rem;
    margin-top: 3.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--panel-border);
    letter-spacing: 0.02em;
}

div[data-testid="stExpander"] {
    background: var(--panel);
    border: 1px solid var(--panel-border);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# STATE
# ---------------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None

# If a chip was clicked on the previous run, apply it to the widget
# BEFORE the widget is instantiated this run.
if "pending_topic" in st.session_state:
    st.session_state.topic_input = st.session_state.pop("pending_topic")

SAMPLE_TOPICS = ["LLM agents 2026", "CRISPR gene editing", "Fusion energy progress"]

STAGES = [
    ("01", "Search Agent", "Gathers recent web information"),
    ("02", "Reader Agent", "Scrapes & extracts deep content"),
    ("03", "Writer Chain", "Drafts the full research report"),
    ("04", "Critic Chain", "Reviews & scores the report"),
]

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
st.markdown('<div class="eyebrow">MULTI-AGENT AI SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title"><span class="a">Research</span><span class="b">Mind</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Four specialized AI agents collaborate — searching, scraping, '
    'writing, and critiquing — to deliver a polished research report on any topic.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------------
left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown('<div class="section-label">RESEARCH TOPIC</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Research topic",
        key="topic_input",
        placeholder="e.g. Quantum computing breakthroughs in 2026",
        label_visibility="collapsed",
    )

    run_clicked = st.button(
        "✨  Run Research Pipeline",
        type="primary",
        disabled=not topic.strip(),
        use_container_width=True,
    )

    st.markdown('<div class="try-label">TRY →</div>', unsafe_allow_html=True)
    chip_cols = st.columns(len(SAMPLE_TOPICS))
    for col, sample in zip(chip_cols, SAMPLE_TOPICS):
        with col:
            if st.button(sample, key=f"chip_{sample}", use_container_width=True):
                st.session_state.pending_topic = sample
                st.rerun()

with right:
    st.markdown('<div class="panel-title">Pipeline</div>', unsafe_allow_html=True)
    pipeline_placeholder = st.empty()

    def render_pipeline(active_idx=-1, done=False):
        html = ""
        for i, (num, name, desc) in enumerate(STAGES):
            if done:
                cls, status = "done", "COMPLETE"
            elif i == active_idx:
                cls, status = "active", "RUNNING"
            elif i < active_idx:
                cls, status = "done", "COMPLETE"
            else:
                cls, status = "", "WAITING"
            html += f"""
            <div class="pipe-card {cls}">
                <div class="pipe-left">
                    <div class="pipe-num">{num}</div>
                    <div>
                        <div class="pipe-name">{name}</div>
                        <div class="pipe-desc">{desc}</div>
                    </div>
                </div>
                <div class="pipe-status">{status}</div>
            </div>
            """
        pipeline_placeholder.markdown(html, unsafe_allow_html=True)

    render_pipeline()

# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------
if run_clicked and topic.strip():
    with right:
        render_pipeline(active_idx=1)
    with st.spinner("Running the research pipeline... this can take a minute or two."):
        try:
            result = run_research_pipeline(topic.strip())
            st.session_state.result = result
            with right:
                render_pipeline(done=True)
        except Exception as e:
            st.session_state.result = None
            st.error(f"Pipeline failed: {e}")

# ---------------------------------------------------------------------------
# RESULTS
# ---------------------------------------------------------------------------
if st.session_state.result:
    state = st.session_state.result
    st.markdown("---")

    st.markdown(
        f'<div class="result-card"><div class="result-title">📄 Report</div>'
        f'<div class="result-body">{state.get("report", "No report generated.")}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="result-card"><div class="result-title">🧐 Critic Feedback</div>'
        f'<div class="result-body">{state.get("feedback", "No feedback generated.")}</div></div>',
        unsafe_allow_html=True,
    )

    with st.expander("🔍 Raw search results"):
        st.text(state.get("search_result", ""))
    with st.expander("📖 Scraped content"):
        st.text(state.get("scrape_content", ""))

st.markdown(
    '<div class="footer">ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit</div>',
    unsafe_allow_html=True,
)