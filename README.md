# 📄 AI CV Reviewer

An AI-powered CV/Resume reviewer built with Streamlit and Groq (free AI API).  
Upload your CV and get an instant score, feedback, ATS keywords, and improved bullet points.

## Features
- Upload PDF or DOCX
- AI score (0–100) with grade badge
- Section-by-section feedback (Summary, Experience, Skills, Education)
- ATS keyword suggestions tailored to your target job title
- Top 3 bullet point rewrites
- Download full report as .txt

---

## Setup Guide

### 1. Download the project
Download or clone this folder to your computer.

### 2. Get a free Groq API key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account (no credit card needed)
3. Navigate to **API Keys** → click **Create API Key**
4. Copy the key - you'll need it in Step 5

### 3. Create a virtual environment
Open a terminal (PowerShell on Windows, Terminal on Mac/Linux) inside the project folder, then run:

```bash
python -m venv venv
```

Activate it:
```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal line.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Add your API key
Create a file named `.env` in the project root folder (same level as `app.py`) and add:

```
GROQ_API_KEY=your_key_here
```

Replace `your_key_here` with the key you copied in Step 2.

> ⚠️ Never share or commit this file. It's already in `.gitignore`.

### 6. Run the app
```bash
streamlit run app.py
```

A browser tab will open automatically at `http://localhost:8501`.

---

## How to Use
1. Enter your **target job title** in the sidebar (e.g. `Software Engineer`)
2. Upload your CV as a **PDF or DOCX** file
3. Click **Analyse My CV**
4. Wait ~15–30 seconds for results
5. Optionally download the full report as a `.txt` file

---

## Project Structure
```
ai-cv-reviewer/
├── app.py           # Streamlit UI
├── parser.py        # PDF + DOCX text extraction
├── reviewer.py      # Groq API calls
├── utils.py         # Helpers (grading, report generation)
├── .env             # Your API key (never commit!)
├── requirements.txt
└── README.md
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `streamlit` not recognized | Make sure venv is activated before running |
| `GROQ_API_KEY not found` | Check your `.env` file exists in the project root with the correct key |
| Very little text extracted | Your CV might be image-based (scanned). Use a text-based PDF or DOCX instead |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside the activated venv |