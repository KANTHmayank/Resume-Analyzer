# AI Resume Expert

AI Resume Expert is a Streamlit app that helps analyze a resume against a job description.

## What it does

At a glance, the app works like this:

1. Upload a resume in PDF format.
2. Paste a job description into the text area.
3. The app converts the resume PDF into an image using Poppler.
4. Google Gemini reads the resume content and compares it with the job description.
5. The app returns either:
   - a detailed resume review, or
   - an ATS-style percentage match score

## Requirements

To run the project locally or deploy it to Streamlit Cloud, you need:

- Python 3.12+
- Streamlit
- `pdf2image`
- Poppler installed and available on PATH, or installed through `packages.txt` on Streamlit Cloud
- A valid `GEMINI_API_KEY`

## Local run

```powershell
.\.venv\Scripts\python.exe -m streamlit run main.py
```

## Deployment notes

- `requirements.txt` installs the Python dependencies.
- `packages.txt` installs Poppler on Streamlit Cloud.
- Add your API key as a secret in Streamlit Cloud instead of hardcoding it in the app.
