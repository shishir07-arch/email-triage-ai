# Email Triage Assistant

A small tool I built that takes customer support emails and figures out what type of issue it is, how urgent it is, and who on the team should handle it — using Google Gemini.

---

## Setup

### 1. Clone the repo
```
git clone <https://github.com/shishir07-arch/email-triage-ai.git>
cd email-triage-ai
```

### 2. Install the required libraries
```
pip install streamlit google-generativeai python-dotenv
```

### 3. Add your API key
Create a `.env` file in the project folder and add this line:
```
GEMINI_API_KEY=your_key_here
```
You can get a free key from https://aistudio.google.com

### 4. Run it
```
streamlit run app.py
```

## How it works

1. Add your team members and their roles in the sidebar
2. Paste a support email into the text box
3. Hit Analyse Email
4. The AI reads it and tells you the category, urgency, and who to assign it to

---

## Environment Variables

`GEMINI_API_KEY` — your Gemini API key, get it from aistudio.google.com
