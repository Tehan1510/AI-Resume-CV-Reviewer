import re
from datetime import datetime


def clean_text(text: str) -> str:
    """Remove excessive whitespace from extracted CV text."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def get_grade(score: int) -> tuple[str, str]:
    """Returns (grade_letter, color_hex) based on score."""
    if score >= 90:
        return "A+", "#22c55e"
    elif score >= 80:
        return "A", "#4ade80"
    elif score >= 70:
        return "B", "#86efac"
    elif score >= 60:
        return "C", "#facc15"
    elif score >= 50:
        return "D", "#fb923c"
    else:
        return "F", "#ef4444"


def build_report(
    score: int,
    summary: str,
    section_fb: dict,
    keywords: list[str],
    bullets: list[dict],
    job_title: str,
) -> str:
    """Builds a plain-text downloadable report."""
    grade, _ = get_grade(score)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "=" * 60,
        "           AI CV REVIEW REPORT",
        f"           Generated: {now}",
        "=" * 60,
        "",
        f"OVERALL SCORE: {score}/100  (Grade: {grade})",
        "",
        "SUMMARY",
        "-" * 40,
        summary,
        "",
        "SECTION-BY-SECTION FEEDBACK",
        "-" * 40,
    ]

    for section, feedback in section_fb.items():
        lines += [f"\n[{section}]", feedback]

    lines += [
        "",
        f"ATS KEYWORDS TO ADD (for '{job_title}')",
        "-" * 40,
    ]
    for kw in keywords:
        lines.append(f"  • {kw}")

    lines += [
        "",
        "TOP 3 BULLET POINT REWRITES",
        "-" * 40,
    ]
    for i, b in enumerate(bullets, 1):
        lines += [
            f"\n{i}. ORIGINAL:",
            f"   {b.get('original', '')}",
            "   REWRITTEN:",
            f"   {b.get('rewritten', '')}",
        ]

    lines += ["", "=" * 60, "End of Report"]
    return "\n".join(lines)