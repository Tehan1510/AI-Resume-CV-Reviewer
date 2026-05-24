# AI CV Reviewer

AI-powered CV/Resume reviewer built with Streamlit + Claude API.

## Features
- Upload PDF or DOCX
- AI score (0–100) with grade badge
- Section-by-section feedback
- ATS keyword suggestions
- Top 3 bullet point rewrites
- Download full report as .txt

## Setup

1. **Clone / download** the project folder.

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key:**
   - Copy `.env.example` → `.env`
   - Paste your Anthropic API key inside

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Project Structure
```
ai-cv-reviewer/
├── app.py          # Streamlit UI
├── parser.py       # PDF + DOCX text extraction
├── reviewer.py     # Claude API calls
├── utils.py        # Helpers (grading, report generation)
├── .env            # Your API key (never commit!)
├── requirements.txt
└── README.md
```