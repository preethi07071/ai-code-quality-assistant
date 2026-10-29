from flask import Flask, render_template, request, jsonify
from analyzer import analyze_code

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "")
    language = data.get("language", "python").lower()
    if not code.strip():
        return jsonify({"error": "Paste some code before analyzing it."}), 400
    if len(code) > 50000:
        return jsonify({"error": "Please keep the submitted code under 50,000 characters."}), 413
    if language not in {"python", "java", "javascript"}:
        return jsonify({"error": "Choose Python, Java, or JavaScript."}), 400
    return jsonify(analyze_code(code, language))

if __name__ == "__main__":
    app.run(debug=True)
