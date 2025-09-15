from flask import Flask, request, jsonify, render_template
import re
from collections import Counter

app = Flask(__name__)

def word_stats(text: str):
    # Lowercase and extract "words"
    words = re.findall(r"\b\w+\b", text.lower())
    total = len(words)
    counts = Counter(words)
    unique = len(counts)
    return total, unique, counts

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    text = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        total, unique, counts = word_stats(text)
        result = {
            "total_words": total,
            "unique_words": unique,
            "top_5": counts.most_common(5)
        }
    return render_template("index.html", result=result, text=text)

@app.route("/api/wordcount", methods=["POST"])
def api_wordcount():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    total, unique, counts = word_stats(text)
    return jsonify({
        "total_words": total,
        "unique_words": unique,
        "counts": counts
    })

if __name__ == "__main__":
    # Listen on all interfaces so EC2/browser can reach it
    app.run(host="0.0.0.0", port=8080, debug=True)
