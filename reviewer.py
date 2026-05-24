import anthropic
import json
import re

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env automatically
MODEL = "claude-sonnet-4-20250514"


def _ask_claude(prompt: str, max_tokens: int = 1500) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def score_cv(cv_text: str) -> dict:
    """Returns {"score": int, "summary": str}"""
    prompt = f"""You are an expert HR recruiter and career coach. Analyze this CV and return ONLY valid JSON (no markdown, no extra text) in this exact format:
{{
  "score": <integer 0-100>,
  "summary": "<2-3 sentence overall assessment>"
}}

CV:
{cv_text[:4000]}"""
    
    raw = _ask_claude(prompt, max_tokens=300)
    # Strip any accidental markdown fences
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


def section_feedback(cv_text: str) -> dict:
    """Returns feedback for Summary, Experience, Skills, Education."""
    prompt = f"""You are an expert CV reviewer. Analyze this CV and return ONLY valid JSON (no markdown) in this exact format:
{{
  "Summary": "<feedback on the professional summary/objective section>",
  "Experience": "<feedback on work experience section>",
  "Skills": "<feedback on skills section>",
  "Education": "<feedback on education section>"
}}

If a section is missing, say "Section not found — consider adding this."

CV:
{cv_text[:4000]}"""

    raw = _ask_claude(prompt, max_tokens=800)
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


def ats_keywords(cv_text: str, job_title: str) -> list[str]:
    """Returns list of 10 ATS keyword suggestions."""
    prompt = f"""You are an ATS optimization expert. For a "{job_title}" role, list exactly 10 keywords/phrases that are commonly scanned by ATS systems and are MISSING or underrepresented in this CV.

Return ONLY a JSON array of strings, no other text. Example: ["keyword1", "keyword2"]

CV:
{cv_text[:3000]}"""

    raw = _ask_claude(prompt, max_tokens=300)
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


def rewrite_bullets(cv_text: str) -> list[dict]:
    """Returns top 3 bullet rewrites as [{"original": ..., "rewritten": ...}]"""
    prompt = f"""You are a professional CV writer. Find the 3 weakest bullet points in this CV and rewrite them to be stronger (using action verbs, quantified results, and impact).

Return ONLY valid JSON array (no markdown) in this exact format:
[
  {{"original": "<original bullet>", "rewritten": "<improved bullet>"}},
  {{"original": "<original bullet>", "rewritten": "<improved bullet>"}},
  {{"original": "<original bullet>", "rewritten": "<improved bullet>"}}
]

CV:
{cv_text[:4000]}"""

    raw = _ask_claude(prompt, max_tokens=600)
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)