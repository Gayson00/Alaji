from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load brain file
def load_brain():
    path = os.path.join(os.path.dirname(__file__), "..", "brain.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

BRAIN_DATA = load_brain()

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "Flask API on Vercel is running!"
    })

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    user_msg = data.get("msg", "")

    if not user_msg.strip():
        return jsonify({"error": "Babu sakon da aka turo"}), 400

    reply = f"Na karɓi sakonka: {user_msg}. Na kuma karanta brain.txt (chars: {len(BRAIN_DATA)})."

    return jsonify({"reply": reply})

# ---- Vercel entrypoint ----
def handler(request):
    return app(request.environ, start_response=lambda *args: None)