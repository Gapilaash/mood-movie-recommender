# Mood Movie Recommender

Unga mood-ku match aana movies AI suggest pannum website. Tamil, English, Hindi, Telugu, Malayalam — language select pannalam.

## Setup Steps

1. Terminal open pannunga, idha run pannunga:
```
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

2. `.env.example` file-a `.env` nu rename pannunga, [ai.google.dev](https://ai.google.dev) la irundhu free API key edutthu, andha file-la paste pannunga:
```
GEMINI_API_KEY=your_actual_key_here
```

3. App run pannunga:
```
python app.py
```

4. Browser-la open pannunga:
```
http://127.0.0.1:5000
```

## Files

- `app.py` — Flask backend, Gemini AI call pannudhu
- `templates/index.html` — Frontend UI (mood input + language dropdown + results)
- `requirements.txt` — Python packages needed
- `.env` — Unga API key (idha GitHub-la push pannadhinga, private-ah vainga)

## Free Deploy Panna

Render.com or PythonAnywhere use pannunga — free tier-la deploy pannalam.
