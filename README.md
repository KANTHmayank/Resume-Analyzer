## AI Resume Expert

This is a Streamlit app that analyzes a resume PDF against a job description and returns:

- a resume review
- an ATS-style match score

### Deployment on Streamlit Community Cloud

1. Push this `week1/day4` project to GitHub.
2. In Streamlit Cloud, create a new app and point it to `main.py`.
3. Add your secrets in the app settings:

	- `GEMINI_API_KEY` = your Gemini API key
	- optional: `GEMINI_MODEL` = `gemini-3.5-flash`

4. Keep `requirements.txt` in the repo root so Streamlit installs the Python packages.
5. Keep `packages.txt` in the repo root so Streamlit installs Poppler on the host.

### Local run

```powershell
.\.venv\Scripts\python.exe -m streamlit run main.py
```
