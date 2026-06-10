import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@300;400;500&family=Inter:wght@300;400;500&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #ffffff !important;
    background: #080c18;
}

/* ── NUCLEAR WHITE TEXT — covers every Streamlit markdown element ── */
p, li, ul, ol, span, div, h1, h2, h3, h4, h5, h6,
strong, em, b, i, a, code, pre, blockquote, td, th, tr,
label, small, caption, figcaption, summary {
    color: #ffffff !important;
}

/* Target Streamlit's internal rendered markdown containers */
.stMarkdown *, 
[data-testid="stMarkdownContainer"] *,
[data-testid="stVerticalBlock"] p,
[data-testid="stVerticalBlock"] li,
[data-testid="stVerticalBlock"] h1,
[data-testid="stVerticalBlock"] h2,
[data-testid="stVerticalBlock"] h3,
[data-testid="stVerticalBlock"] h4,
[data-testid="stVerticalBlock"] span,
[data-testid="stVerticalBlock"] strong,
[data-testid="stVerticalBlock"] em,
.element-container *,
.stText *,
section[data-testid="stSidebar"] *,
.main .block-container * {
    color: #ffffff !important;
}

/* Expander header and content */
[data-testid="stExpander"] *,
details summary *,
details *,
.streamlit-expanderHeader *,
.streamlit-expanderContent * {
    color: #ffffff !important;
}

/* Spinner text */
[data-testid="stSpinner"] *,
.stSpinner * {
    color: #ffffff !important;
}

/* Warning / info / error boxes */
[data-testid="stAlert"] *,
.stAlert * {
    color: #ffffff !important;
}
.stApp {
    background: #080c18;
    background-image:
        radial-gradient(ellipse 120% 60% at 50% -20%, rgba(91,106,249,0.12) 0%, transparent 55%),
        radial-gradient(ellipse 50% 80% at 95% 60%, rgba(52,211,153,0.05) 0%, transparent 45%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 3rem 4rem 6rem;
    max-width: 1100px;
    margin: 0 auto;
}

/* ── Wordmark ── */
.wordmark {
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
    margin-bottom: 0.5rem;
}
.wordmark-icon {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    color: #5b6af9;
    letter-spacing: -0.02em;
}
.wordmark-text {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ── Hero headline ── */
.hero-headline {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #ffffff;
    margin: 1.2rem 0 0.8rem;
}
.hero-headline em {
    font-style: normal;
    color: #5b6af9;
}
.hero-body {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    font-weight: 300;
    color: #b0bcd8;
    line-height: 1.65;
    max-width: 520px;
    margin-bottom: 2.5rem;
}

/* ── Input area ── */
.input-row {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
    margin-bottom: 0.75rem;
}

/* Override Streamlit text input */
.stTextInput > label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #5b6af9 !important;
    margin-bottom: 0.4rem !important;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(91,106,249,0.25) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
    height: 52px !important;
}
.stTextInput > div > div > input::placeholder {
    color: #4a5580 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #5b6af9 !important;
    box-shadow: 0 0 0 3px rgba(91,106,249,0.15) !important;
    outline: none !important;
}

/* ── Run button ── */
.stButton > button {
    background: #5b6af9 !important;
    color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0 2rem !important;
    height: 52px !important;
    cursor: pointer !important;
    transition: background 0.2s, transform 0.1s, box-shadow 0.2s !important;
    box-shadow: 0 4px 20px rgba(91,106,249,0.35) !important;
    white-space: nowrap !important;
}
.stButton > button:hover {
    background: #6e7dff !important;
    box-shadow: 0 6px 28px rgba(91,106,249,0.5) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Chips row ── */
.chips-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: #2e3650;
    text-transform: uppercase;
    margin-right: 0.4rem;
}
.chip {
    display: inline-block;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 0.22rem 0.75rem;
    font-size: 0.76rem;
    color: #8a97b8;
    font-family: 'Inter', sans-serif;
    margin-right: 0.4rem;
}

/* ── Thin divider ── */
.thin-rule {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(91,106,249,0.25) 30%, rgba(91,106,249,0.25) 70%, transparent 100%);
    margin: 2.5rem 0;
}

/* ── Pipeline rail ── */
.pipeline-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #2e3650;
    margin-bottom: 1.4rem;
}

.pipeline-rail {
    display: grid;
    grid-template-columns: 1fr 28px 1fr 28px 1fr 28px 1fr;
    align-items: center;
    gap: 0;
    margin-bottom: 2rem;
}

.pipeline-connector {
    height: 2px;
    background: #141929;
    border-radius: 2px;
    position: relative;
    overflow: hidden;
}
.pipeline-connector.active-conn {
    background: rgba(91,106,249,0.5);
}
.pipeline-connector.done-conn {
    background: rgba(52,211,153,0.5);
}

.agent-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.2rem 1rem 1rem;
    position: relative;
    transition: border-color 0.3s, background 0.3s;
    min-height: 110px;
}
.agent-card.state-active {
    border-color: rgba(91,106,249,0.45);
    background: rgba(91,106,249,0.06);
}
.agent-card.state-done {
    border-color: rgba(52,211,153,0.3);
    background: rgba(52,211,153,0.04);
}

.agent-icon {
    font-size: 1.3rem;
    margin-bottom: 0.55rem;
    display: block;
}
.agent-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #ffffff;
    display: block;
    margin-bottom: 0.15rem;
}
.agent-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: #6b7a99;
    line-height: 1.4;
    display: block;
    margin-bottom: 0.6rem;
}
.agent-badge {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    border: 1px solid transparent;
}
.badge-waiting {
    color: #2e3650;
    border-color: rgba(255,255,255,0.05);
    background: transparent;
}
.badge-running {
    color: #5b6af9;
    border-color: rgba(91,106,249,0.35);
    background: rgba(91,106,249,0.08);
    animation: pulse-badge 1.4s ease-in-out infinite;
}
.badge-done {
    color: #34d399;
    border-color: rgba(52,211,153,0.3);
    background: rgba(52,211,153,0.07);
}
@keyframes pulse-badge {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* ── Results section ── */
.results-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin-bottom: 1.5rem;
}

/* Expander override */
.streamlit-expanderHeader {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    color: #4a5470 !important;
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 8px !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.015) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    color: #7a8aaa !important;
    line-height: 1.7 !important;
}

/* ── Report card ── */
.report-card {
    background: rgba(91,106,249,0.04);
    border: 1px solid rgba(91,106,249,0.2);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.2rem;
}
.report-card-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5b6af9;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.report-card-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(91,106,249,0.2);
}
/* markdown inside report */
.report-card h1, .report-card h2, .report-card h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #ffffff !important;
}
.report-card p, .report-card li {
    font-family: 'Inter', sans-serif !important;
    color: #d0d8f0 !important;
    line-height: 1.8 !important;
}

/* ── Critic card ── */
.critic-card {
    background: rgba(52,211,153,0.03);
    border: 1px solid rgba(52,211,153,0.18);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.2rem;
}
.critic-card-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #34d399;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.critic-card-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(52,211,153,0.18);
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid rgba(91,106,249,0.3) !important;
    color: #5b6af9 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    border-radius: 8px !important;
    padding: 0.45rem 1.2rem !important;
    transition: background 0.2s, border-color 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(91,106,249,0.08) !important;
    border-color: rgba(91,106,249,0.5) !important;
}

/* ── Footer ── */
.footer {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: #1e2538;
    text-align: center;
    margin-top: 5rem;
}

/* ── Warning ── */
.stWarning {
    background: rgba(249,183,91,0.08) !important;
    border: 1px solid rgba(249,183,91,0.2) !important;
    border-radius: 8px !important;
    color: #b89050 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Agent metadata ─────────────────────────────────────────────────────────────
AGENTS = [
    ("search", "◎", "Search",  "Finds recent, reliable web sources"),
    ("reader", "◉", "Reader",  "Scrapes & extracts deep content"),
    ("writer", "◈", "Writer",  "Drafts the full research report"),
    ("critic", "◆", "Critic",  "Reviews & scores the draft"),
]

def get_state(key):
    r = st.session_state.results
    steps = [a[0] for a in AGENTS]
    if key in r:
        return "done"
    if st.session_state.running:
        for k in steps:
            if k not in r:
                return "running" if k == key else "waiting"
    return "waiting"


# ── Wordmark ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="wordmark">
    <span class="wordmark-icon">◈</span>
    <span class="wordmark-text">ResearchMind</span>
</div>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-headline">Four agents.<br><em>One report.</em></div>
<p class="hero-body">
    Enter a topic and watch a coordinated pipeline of AI agents search, read,
    write, and critique — delivering a polished research brief in minutes.
</p>
""", unsafe_allow_html=True)


# ── Input ──────────────────────────────────────────────────────────────────────
col_in, col_btn = st.columns([5, 1.3])
with col_in:
    topic = st.text_input(
        "TOPIC",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
with col_btn:
    st.markdown("<div style='height:1.78rem'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run pipeline →", use_container_width=True)

# Example chips
st.markdown("""
<div style="margin-top:0.6rem;margin-bottom:0.5rem;">
    <span class="chips-label">Try</span>
    <span class="chip">LLM agents 2025</span>
    <span class="chip">CRISPR gene editing</span>
    <span class="chip">Fusion energy progress</span>
</div>
""", unsafe_allow_html=True)


# ── Thin rule ──────────────────────────────────────────────────────────────────
st.markdown('<div class="thin-rule"></div>', unsafe_allow_html=True)


# ── Pipeline Rail ──────────────────────────────────────────────────────────────
st.markdown('<div class="pipeline-label">Agent Pipeline</div>', unsafe_allow_html=True)

# Build connector classes
def conn_cls(left_key, right_key):
    l_state = get_state(left_key)
    if l_state == "done":
        return "done-conn"
    r_state = get_state(right_key)
    if r_state == "running":
        return "active-conn"
    return ""

badge_labels = {"waiting": "— idle", "running": "● running", "done": "✓ done"}

rail_html = '<div class="pipeline-rail">'
for i, (key, icon, name, desc) in enumerate(AGENTS):
    state = get_state(key)
    card_cls = f"state-{state}" if state != "waiting" else ""
    badge_cls = f"badge-{state}"
    badge_text = badge_labels[state]

    rail_html += f"""
    <div class="agent-card {card_cls}">
        <span class="agent-icon">{icon}</span>
        <span class="agent-name">{name}</span>
        <span class="agent-desc">{desc}</span>
        <span class="agent-badge {badge_cls}">{badge_text}</span>
    </div>
    """
    if i < len(AGENTS) - 1:
        next_key = AGENTS[i + 1][0]
        cc = conn_cls(key, next_key)
        rail_html += f'<div class="pipeline-connector {cc}"></div>'

rail_html += '</div>'
st.markdown(rail_html, unsafe_allow_html=True)


# ── Trigger / run ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Enter a research topic to begin.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    with st.spinner("Search agent is gathering sources…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("Reader agent is extracting content…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("Writer is drafting your report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    with st.spinner("Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results ────────────────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="thin-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="results-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("◎ Search Agent · raw output"):
            st.markdown(r["search"])

    if "reader" in r:
        with st.expander("◉ Reader Agent · raw output"):
            st.markdown(r["reader"])

    if "writer" in r:
        st.markdown("""
        <div class="report-card">
            <div class="report-card-label">◈ Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            label="↓  Download report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    if "critic" in r:
        st.markdown("""
        <div class="critic-card">
            <div class="critic-card-label">◆ Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    RESEARCHMIND · LANGCHAIN MULTI-AGENT · STREAMLIT
</div>
""", unsafe_allow_html=True)