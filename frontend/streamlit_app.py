import html
import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# APPLICATION IMPORTS
# ============================================================

from app.llm.analyzer import ComplaintAnalyzer
from app.llm.resolver import ResolutionSupportGenerator


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Complaint Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HELPERS
# ============================================================

def render_html(markup: str):
    """
    Render HTML in Streamlit without Markdown mistaking it for code.

    Every line is stripped and blank lines are removed, so indented
    tags can never become a Markdown code block.
    """
    cleaned = "\n".join(
        line.strip() for line in markup.splitlines() if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


def esc(value) -> str:
    """Escape any value (e.g. LLM output) for safe use inside HTML."""
    return html.escape(str(value))


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* GLOBAL */
    .stApp {
        background-color: #f5f7fb;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* HERO */
    .hero {
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.10);
    }

    .hero-title {
        color: #ffffff;
        font-size: 2.3rem;
        font-weight: 750;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.6;
        margin: 0;
    }

    /* METRIC CARDS */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.25rem;
        min-height: 120px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }

    .metric-label {
        color: #6b7280;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        color: #111827;
        font-size: 1.45rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .metric-description {
        color: #9ca3af;
        font-size: 0.76rem;
        line-height: 1.4;
    }

    /* SECTION HEADERS */
    .section-title {
        color: #111827;
        font-size: 1.3rem;
        font-weight: 750;
        margin-top: 1.8rem;
        margin-bottom: 0.35rem;
    }

    .section-subtitle {
        color: #6b7280;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* RESULT CARDS */
    .result-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.25rem;
        min-height: 125px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }

    .result-label {
        color: #6b7280;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    .result-value {
        color: #111827;
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 0.55rem;
        line-height: 1.35;
    }

    /* ENTITY CARDS */
    .entity-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.85rem;
        margin-bottom: 0.7rem;
        min-height: 75px;
    }

    .entity-name {
        color: #6b7280;
        font-size: 0.72rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .entity-value {
        color: #111827;
        font-size: 0.92rem;
        font-weight: 650;
        margin-top: 0.3rem;
    }

    /* RESPONSE CARD */
    .response-card {
        background: #ffffff;
        border-left: 4px solid #4f46e5;
        border-top: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
        border-bottom: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.3rem 1.5rem;
        line-height: 1.65;
        color: #374151;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }

    /* PIPELINE */
    .pipeline-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        min-height: 120px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }

    .pipeline-icon {
        font-size: 1.8rem;
        margin-bottom: 0.4rem;
    }

    .pipeline-title {
        color: #111827;
        font-size: 0.9rem;
        font-weight: 700;
    }

    .pipeline-description {
        color: #9ca3af;
        font-size: 0.72rem;
        margin-top: 0.25rem;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    /* BUTTONS */
    .stButton > button {
        border-radius: 9px;
        font-weight: 650;
        min-height: 42px;
    }

    /* TEXT AREA */
    textarea {
        border-radius: 10px !important;
    }

    /* FOOTER */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.78rem;
        padding: 2rem 0 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD COMPONENTS
# ============================================================

@st.cache_resource
def load_components():
    analyzer = ComplaintAnalyzer()
    resolver = ResolutionSupportGenerator()
    return analyzer, resolver


analyzer, resolver = load_components()


# ============================================================
# SESSION STATE
# ============================================================

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "resolution" not in st.session_state:
    st.session_state.resolution = None

if "complaint" not in st.session_state:
    st.session_state.complaint = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <h2 style="color:white; margin-bottom:0;">🧠 CCI</h2>
        <p style="color:#94a3b8; margin-top:4px;">
            Customer Complaint Intelligence
        </p>
        """
    )

    st.divider()

    st.markdown("### System Overview")

    st.markdown(
        """
**NLP Layer**

• Sentiment Analysis  
• Named Entity Recognition  

**LLM Layer**

• Complaint Classification  
• Intent Detection  
• Urgency Detection  
• Resolution Generation  

**API Layer**

• FastAPI  
• Structured JSON
"""
    )

    st.divider()

    st.markdown("### Technology Stack")

    st.markdown(
        """
`Python`

`FastAPI`

`Streamlit`

`spaCy`

`Transformers`

`Groq`
"""
    )

    st.divider()

    st.caption("NLP + LLM powered customer support intelligence")


# ============================================================
# HERO
# ============================================================

render_html(
    """
    <div class="hero">
        <div class="hero-title">Customer Complaint Intelligence</div>
        <p class="hero-subtitle">
            Transform unstructured customer complaints into
            actionable intelligence using Natural Language
            Processing and Large Language Models.
        </p>
    </div>
    """
)


# ============================================================
# KPI CARDS
# ============================================================

columns = st.columns(4)

metrics = [
    ("NLP ENGINE", "Active", "Sentiment + Entity Extraction"),
    ("LLM ENGINE", "Groq", "Context-aware complaint analysis"),
    ("ANALYSIS", "4 Signals", "Category · Intent · Sentiment · Urgency"),
    ("OUTPUT", "Actionable", "Resolution support for agents"),
]

for column, (label, value, description) in zip(columns, metrics):
    with column:
        render_html(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-description">{description}</div>
            </div>
            """
        )


# ============================================================
# INPUT SECTION
# ============================================================

render_html(
    """
    <div class="section-title">Analyze a Customer Complaint</div>
    <div class="section-subtitle">
        Enter a complaint or select an example below.
        The system will identify the issue, assess urgency,
        extract important information, and generate
        resolution support.
    </div>
    """
)


# ============================================================
# EXAMPLE COMPLAINTS
# ============================================================

examples = {
    "Late Delivery": (
        "My laptop was supposed to arrive five days ago. "
        "I already paid for it but haven't received it. "
        "Customer support hasn't responded to my messages."
    ),
    "Refund Issue": (
        "I returned my headphones two weeks ago but I still "
        "haven't received my refund. The payment was made "
        "using my credit card."
    ),
    "Technical Problem": (
        "The application crashes every time I try to upload "
        "a document. I have tried restarting it several times "
        "but the problem continues."
    ),
}

example_columns = st.columns(3)

with example_columns[0]:
    if st.button("📦  Late Delivery", use_container_width=True):
        st.session_state.complaint = examples["Late Delivery"]
        st.rerun()

with example_columns[1]:
    if st.button("💳  Refund Issue", use_container_width=True):
        st.session_state.complaint = examples["Refund Issue"]
        st.rerun()

with example_columns[2]:
    if st.button("💻  Technical Problem", use_container_width=True):
        st.session_state.complaint = examples["Technical Problem"]
        st.rerun()


# ============================================================
# TEXT INPUT
# ============================================================

complaint = st.text_area(
    "Customer complaint",
    value=st.session_state.complaint,
    height=155,
    placeholder=(
        "Example: My order was supposed to arrive "
        "last week, but I still haven't received it..."
    ),
    label_visibility="collapsed",
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "🔍  Analyze Complaint",
    type="primary",
    use_container_width=True,
)


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_button:

    if not complaint.strip():
        st.warning("Please enter a customer complaint first.")

    else:
        st.session_state.complaint = complaint

        with st.spinner("Analyzing complaint with NLP and Groq..."):
            try:
                # Component 1 + 2
                analysis = analyzer.analyze(complaint)

                # Component 3
                resolution = resolver.generate(
                    complaint=complaint,
                    analysis=analysis,
                )

                # Save results
                st.session_state.analysis = analysis
                st.session_state.resolution = resolution

                st.success("Complaint analyzed successfully.")

            except Exception as exc:
                st.error(f"Analysis failed: {exc}")


# ============================================================
# RESULTS
# ============================================================

if (
    st.session_state.analysis is not None
    and st.session_state.resolution is not None
):

    analysis = st.session_state.analysis
    resolution = st.session_state.resolution

    # --------------------------------------------------------
    # COMPLAINT INTELLIGENCE
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-title">Complaint Intelligence</div>
        <div class="section-subtitle">
            Structured insights generated from the complaint.
        </div>
        """
    )

    result_columns = st.columns(4)

    result_cards = [
        ("CATEGORY", analysis.category),
        ("INTENT", analysis.intent),
        ("SENTIMENT", analysis.sentiment),
        ("URGENCY", analysis.urgency),
    ]

    for column, (label, value) in zip(result_columns, result_cards):
        with column:
            render_html(
                f"""
                <div class="result-card">
                    <div class="result-label">{label}</div>
                    <div class="result-value">{esc(value)}</div>
                </div>
                """
            )

    # --------------------------------------------------------
    # EXTRACTED ENTITIES
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-title">Extracted Information</div>
        <div class="section-subtitle">
            Key entities identified from the customer complaint.
        </div>
        """
    )

    entities = analysis.entities.model_dump()

    entity_columns = st.columns(4)

    for index, (name, value) in enumerate(entities.items()):
        with entity_columns[index % 4]:

            display_value = esc(value) if value else "Not detected"

            render_html(
                f"""
                <div class="entity-card">
                    <div class="entity-name">{esc(name.replace("_", " "))}</div>
                    <div class="entity-value">{display_value}</div>
                </div>
                """
            )

    # --------------------------------------------------------
    # RESOLUTION SUPPORT
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-title">Resolution Support</div>
        <div class="section-subtitle">
            AI-generated support for the customer service agent.
        </div>
        """
    )

    left_column, right_column = st.columns([1, 1])

    with left_column:

        st.markdown("#### 📋 Complaint Summary")
        st.info(resolution.summary)

        st.markdown("#### ✅ Recommended Actions")
        for action in resolution.recommended_actions:
            st.markdown(f"• {action}")

    with right_column:

        st.markdown("#### 💬 Suggested Customer Response")

        safe_response = esc(resolution.suggested_response).replace("\n", "<br>")

        render_html(
            f"""
            <div class="response-card">
                {safe_response}
            </div>
            """
        )

    # --------------------------------------------------------
    # SYSTEM PIPELINE
    # --------------------------------------------------------

    render_html(
        """
        <div class="section-title">How the System Works</div>
        <div class="section-subtitle">
            The complaint passes through multiple NLP and
            LLM stages before producing the final resolution.
        </div>
        """
    )

    pipeline_columns = st.columns(5)

    pipeline = [
        ("📝", "Complaint", "Raw customer text"),
        ("🧠", "NLP", "Sentiment + entities"),
        ("⚡", "Groq LLM", "Contextual analysis"),
        ("📊", "Intelligence", "Category + intent + urgency"),
        ("🎯", "Resolution", "Actions + response"),
    ]

    for column, (icon, title, description) in zip(pipeline_columns, pipeline):
        with column:
            render_html(
                f"""
                <div class="pipeline-card">
                    <div class="pipeline-icon">{icon}</div>
                    <div class="pipeline-title">{title}</div>
                    <div class="pipeline-description">{description}</div>
                </div>
                """
            )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        Customer Complaint Intelligence
        &nbsp; • &nbsp;
        NLP + LLM Powered Analysis
    </div>
    """
)