import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env before any API calls

from parser import parse_cv
from reviewer import score_cv, section_feedback, ats_keywords, rewrite_bullets
from utils import clean_text, get_grade, build_report

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI CV Reviewer",
    page_icon="📄",
    layout="centered",
)

st.title("📄 AI CV Reviewer")
st.caption("Upload your CV and get instant AI-powered feedback.")

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    job_title = st.text_input(
        "Target Job Title",
        placeholder="e.g. Software Engineer",
        help="Used to generate ATS keyword suggestions tailored to the role.",
    )
    st.markdown("---")
    st.info("Your CV text is only sent to the Groq API and is not stored.")

# ── File upload ───────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload your CV (PDF or DOCX)",
    type=["pdf", "docx"],
    help="Max ~5 MB recommended.",
)

if uploaded_file and st.button("🔍 Analyse My CV", type="primary"):

    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY not found. Add it to your .env file.")
        st.stop()

    # ── Extract text ──────────────────────────────────────────
    with st.spinner("Reading your CV..."):
        try:
            raw_text = parse_cv(uploaded_file)
            cv_text = clean_text(raw_text)
        except Exception as e:
            st.error(f"Could not read file: {e}")
            st.stop()

    if len(cv_text) < 100:
        st.warning("Very little text was extracted. The file might be image-based or empty.")
        st.stop()

    # ── Score ─────────────────────────────────────────────────
    with st.spinner("Scoring your CV..."):
        score_data = score_cv(cv_text)
        score = score_data.get("score", 0)
        summary = score_data.get("summary", "")

    grade, color = get_grade(score)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(
            f"""
            <div style="background:{color};border-radius:12px;padding:20px;text-align:center;">
                <div style="font-size:2.5rem;font-weight:bold;color:white;">{grade}</div>
                <div style="font-size:1.2rem;color:white;">{score}/100</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.subheader("Overall Assessment")
        st.write(summary)

    st.divider()

    # ── Section feedback ──────────────────────────────────────
    with st.spinner("Analysing sections..."):
        sec_fb = section_feedback(cv_text)

    st.subheader("📋 Section-by-Section Feedback")
    icons = {"Summary": "🗒️", "Experience": "💼", "Skills": "🛠️", "Education": "🎓"}
    for section, feedback in sec_fb.items():
        with st.expander(f"{icons.get(section, '📌')} {section}"):
            st.write(feedback)

    st.divider()

    # ── ATS Keywords ──────────────────────────────────────────
    target = job_title.strip() if job_title.strip() else "the target role"
    with st.spinner(f"Finding ATS keywords for '{target}'..."):
        keywords = ats_keywords(cv_text, target)

    st.subheader(f"🔑 ATS Keywords to Add (for '{target}')")
    cols = st.columns(2)
    for i, kw in enumerate(keywords):
        cols[i % 2].markdown(f"✅ {kw}")

    st.divider()

    # ── Bullet rewrites ───────────────────────────────────────
    with st.spinner("Rewriting weak bullets..."):
        bullets = rewrite_bullets(cv_text)

    st.subheader("✍️ Top 3 Bullet Point Rewrites")
    for i, b in enumerate(bullets, 1):
        st.markdown(f"**{i}. Original:**")
        st.error(b.get("original", ""))
        st.markdown("**Rewritten:**")
        st.success(b.get("rewritten", ""))

    st.divider()

    # ── Download report ───────────────────────────────────────
    report_text = build_report(score, summary, sec_fb, keywords, bullets, target)
    st.download_button(
        label="⬇️ Download Full Report (.txt)",
        data=report_text,
        file_name="cv_review_report.txt",
        mime="text/plain",
    )

elif not uploaded_file:
    st.info("👆 Upload a PDF or DOCX file to get started.")