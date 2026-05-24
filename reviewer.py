from groq import Groq
import json
import re
import os
import streamlit as st

api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)
MODEL = "llama-3.3-70b-versatile"


def _ask(prompt: str, max_tokens: int = 1500) -> str:
    msg = client.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.choices[0].message.content.strip()


def _parse(raw: str):
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


def score_cv(cv_text: str) -> dict:
    prompt = f"""You are an expert HR recruiter. Analyze this CV and return ONLY valid JSON, no markdown:
{{"score": <integer 0-100>, "summary": "<2-3 sentence assessment>"}}
CV:
{cv_text[:4000]}"""
    return _parse(_ask(prompt, 300))


def section_feedback(cv_text: str) -> dict:
    prompt = f"""Analyze this CV and return ONLY valid JSON, no markdown:
{{"Summary": "<feedback>", "Experience": "<feedback>", "Skills": "<feedback>", "Education": "<feedback>"}}
If a section is missing, say "Section not found — consider adding this."
CV:
{cv_text[:4000]}"""
    return _parse(_ask(prompt, 800))


def ats_keywords(cv_text: str, job_title: str) -> list[str]:
    prompt = f"""For a "{job_title}" role, list exactly 10 ATS keywords MISSING from this CV.
Return ONLY a JSON array: ["keyword1", "keyword2", ...]
CV:
{cv_text[:3000]}"""
    return _parse(_ask(prompt, 300))


def rewrite_bullets(cv_text: str) -> list[dict]:
    prompt = f"""Find the 3 weakest bullet points in this CV and rewrite them with action verbs and quantified results.
Return ONLY valid JSON array, no markdown:
[{{"original": "...", "rewritten": "..."}}, ...]
CV:
{cv_text[:4000]}"""
    return _parse(_ask(prompt, 600))