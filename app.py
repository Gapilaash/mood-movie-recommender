from flask import Flask, request, jsonify, render_template
from google import genai
from dotenv import load_dotenv
import os
import json
import requests
import urllib.parse

load_dotenv()
app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.1-flash-lite"

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_BASE = "https://www.omdbapi.com/"


def youtube_trailer_search_url(title, year):
    """No API key needed for this — just builds a YouTube search link.
    It won't jump straight to the official trailer, but the top result
    is almost always it."""
    query = f"{title} {year or ''} trailer".strip()
    return f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"


def omdb_enrich(title, year):
    """Look up a movie on OMDb and pull poster, cast and IMDb rating.
    Returns an empty dict (safe no-op) if OMDb isn't configured or the
    movie isn't found, so the app keeps working either way."""
    if not OMDB_API_KEY:
        return {}

    try:
        params = {"apikey": OMDB_API_KEY, "t": title, "type": "movie"}
        if year:
            params["y"] = year
        res = requests.get(OMDB_BASE, params=params, timeout=6)
        res.raise_for_status()
        data = res.json()

        # If the strict title+year lookup failed, retry without the year.
        # The AI sometimes gives a slightly off release year, which makes
        # OMDb's exact-year match miss even when the movie itself exists.
        if data.get("Response") != "True" and year:
            params.pop("y", None)
            res = requests.get(OMDB_BASE, params=params, timeout=6)
            res.raise_for_status()
            data = res.json()

        if data.get("Response") != "True":
            return {}

        poster = data.get("Poster")
        poster_url = poster if poster and poster != "N/A" else None

        actors_raw = data.get("Actors", "")
        cast = [a.strip() for a in actors_raw.split(",") if a.strip()] if actors_raw != "N/A" else []

        rating = data.get("imdbRating")
        imdb_rating = rating if rating and rating != "N/A" else None

        return {
            "poster_url": poster_url,
            "cast": cast[:4],
            "imdb_rating": imdb_rating,
        }
    except requests.RequestException:
        return {}
    except (KeyError, ValueError, TypeError):
        return {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/favorites")
def favorites_page():
    return render_template("favorites.html")


@app.route("/watchlist")
def watchlist_page():
    return render_template("watchlist.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json(force=True)
    mood = data.get("mood", "").strip()
    language = data.get("language", "Any").strip()
    count = int(data.get("count", 5))
    count = max(1, min(count, 10))
    genre = data.get("genre", "Any").strip()
    decade = data.get("decade", "Any").strip()
    exclude = data.get("exclude", [])
    if not isinstance(exclude, list):
        exclude = []
    exclude = [str(t).strip() for t in exclude if str(t).strip()][:30]

    if not mood:
        return jsonify({"error": "Please enter your mood."}), 400

    lang_instruction = f"in {language}" if language != "Any" else "in any language"

    genre_instruction = ""
    if genre and genre != "Any":
        genre_instruction = f"\n    Only suggest movies in the {genre} genre.\n"

    decade_instruction = ""
    if decade and decade != "Any":
        decade_instruction = f"\n    Only suggest movies released in the {decade}.\n"

    exclude_instruction = ""
    if exclude:
        exclude_list = ", ".join(exclude)
        exclude_instruction = f"\n    Do NOT suggest any of these movies again, pick different ones: {exclude_list}\n"

    prompt = f"""
    User's current mood/feeling: "{mood}"

    Suggest {count} movies {lang_instruction} that match this mood perfectly.
    {genre_instruction}{decade_instruction}{exclude_instruction}
    For each movie give:
    - title
    - genre
    - reason (one line on why it fits the mood)
    - year (release year as integer)

    Respond ONLY with a valid JSON array, no extra text, no markdown fences:
    [
      {{"title": "...", "genre": "...", "reason": "...", "year": 2020}}
    ]
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        movies = json.loads(text)

        # Enrich each movie: poster/cast/rating from OMDb (if key set),
        # plus a YouTube trailer search link (always works, no key needed).
        for movie in movies:
            enrichment = omdb_enrich(movie.get("title", ""), movie.get("year"))
            movie.update(enrichment)
            movie["trailer_url"] = youtube_trailer_search_url(movie.get("title", ""), movie.get("year"))

        return jsonify({"result": json.dumps(movies)})
    except json.JSONDecodeError:
        return jsonify({"error": "Could not parse the AI response. Please try again."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


FEEDBACK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.json")


@app.route("/feedback", methods=["POST"])
def feedback():
    """Logs a thumbs up/down rating for a recommended movie to a local
    JSON file. Best-effort only — if it fails, the UI already updated
    optimistically, so we just report a soft failure."""
    data = request.get_json(force=True)
    title = str(data.get("title", "")).strip()
    rating = data.get("rating")
    mood = str(data.get("mood", "")).strip()

    if not title or rating not in ("up", "down"):
        return jsonify({"error": "Invalid feedback payload."}), 400

    entry = {"title": title, "rating": rating, "mood": mood}

    try:
        entries = []
        if os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                try:
                    entries = json.load(f)
                except json.JSONDecodeError:
                    entries = []
        entries.append(entry)
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        return jsonify({"status": "ok"})
    except OSError:
        return jsonify({"status": "not_saved"})


if __name__ == "__main__":
    app.run(debug=True)
