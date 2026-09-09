
# Mood-Based Movie Recommender

An AI-powered website that suggests movies tailored to your current mood. Supports multiple languages including Tamil, English, Hindi, Telugu, and Malayalam.

## Setup Instructions

1. Open your terminal and run the following commands:
```
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

2. Rename `.env.example` to `.env`, then obtain a free API key from [ai.google.dev](https://ai.google.dev) and paste it into the file:
```
GEMINI_API_KEY=your_actual_key_here
```

3. (Optional, but needed for posters/cast/IMDb rating) Get a free OMDb API key:
   - Go to [omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)
   - Select the **FREE** tier (1,000 requests/day, no cost, no card needed)
   - Enter your email — the key is emailed to you instantly
   - Click the activation link in that email (the key won't work until you do this)
   - Add it to your `.env` file:
```
OMDB_API_KEY=your_omdb_key_here
```
   If you skip this step, the app still works — it just won't show posters, cast, or ratings. Trailer search links work either way (no key needed).

   Note: OMDb doesn't provide "where to watch" streaming data. Poster, top cast, and IMDb rating are included; trailer is a YouTube search link rather than a direct link to the exact official trailer.

4. Start the application:
```
python app.py
```

5. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Project Structure

- `app.py` — Flask backend responsible for handling Gemini AI API calls
- `templates/index.html` — Frontend UI comprising the mood input field, language selector, and results display
- `requirements.txt` — Required Python dependencies
- `.env` — Stores your API key; **do not push this file to GitHub** — keep it private

## Free Deployment Options

You can deploy this application at no cost using [Render.com](https://render.com) or [PythonAnywhere](https://www.pythonanywhere.com), both of which offer free hosting tiers.
