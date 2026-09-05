
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

3. Start the application:
```
python app.py
```

4. Open your browser and navigate to:
```
http://127.0.0.1:5000
```


## Project Structure

- `app.py` — Flask backend responsible for handling Gemini AI API calls
- `templates/index.html` — Frontend UI comprising the mood input field, language selector, and results display
- `requirements.txt` — Required Python dependencies
- `.env` — Stores your API key; **do not push this file to GitHub** — keep it private

## Free Deployment Options

You can deploy this application at no cost using [Vercel](https://vercel.com) or [PythonAnywhere](https://www.pythonanywhere.com), both of which offer free hosting tiers.

## Live Demo
🔗 [https://mood-movie-recommender-qdj2.vercel.app](https://mood-movie-recommender-qdj2.vercel.app)
