from flask import Flask, request, jsonify, render_template
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.1-flash-lite"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json(force=True)
    mood = data.get("mood", "").strip()
    language = data.get("language", "Any").strip()

    if not mood:
        return jsonify({"error": "Please enter your mood."}), 400

    lang_instruction = f"in {language}" if language != "Any" else "in any language"

    prompt = f"""
    User's current mood/feeling: "{mood}"

    Suggest 5 movies {lang_instruction} that match this mood perfectly.
    For each movie give:
    - title
    - genre
    - reason (one line on why it fits the mood)

    Respond ONLY with a valid JSON array, no extra text, no markdown fences:
    [
      {{"title": "...", "genre": "...", "reason": "..."}}
    ]
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return jsonify({"result": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
