from flask import Flask, request, jsonify, render_template
import json
import glob
from langdetect import detect

app = Flask(__name__)

IDIOM_DATA_FOLDER = "gemma"

idiom_dict = {}

# ----------------------------------------------------
# LOAD IDIOM FILES (same as infer.py)
# ----------------------------------------------------
print("\n🔍 Loading idiom files...\n")

for file in glob.glob(f"{IDIOM_DATA_FOLDER}/*.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                print(f"⚠ Invalid JSON skipped: {file}")
                continue

            for entry in data:
                idiom = entry.get("idiom", "").strip().lower()
                if idiom:
                    idiom_dict[idiom] = {
                        "literal": entry.get("literal_meaning", "").strip(),
                        "meaning": entry.get("figurative_meaning", "").strip(),
                        "example": entry.get("example", "").strip()
                    }

    except Exception as e:
        print(f"❌ Error reading {file}: {e}")

print(f"✅ Loaded {len(idiom_dict)} idioms.\n")


# ----------------------------------------------------
# LANGUAGE DETECTION
# ----------------------------------------------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"


# ----------------------------------------------------
# FIND IDIOM (same logic as infer.py)
# ----------------------------------------------------
def find_idiom(sentence):
    s = sentence.lower()
    for idiom in idiom_dict:
        if idiom in s:
            return idiom
    return None


# ----------------------------------------------------
# API ROUTE FOR THE WEBSITE
# ----------------------------------------------------
@app.route("/detect", methods=["POST"])
def detect_idiom():
    data = request.json
    sentence = data.get("sentence", "")

    idiom = find_idiom(sentence)
    lang = detect_language(sentence)

    if not idiom:
        return jsonify({
            "status": "not_found",
            "message": "❌ No idiom found."
        })

    entry = idiom_dict[idiom]

    return jsonify({
        "status": "success",
        "idiom": idiom,
        "literal": entry["literal"],
        "meaning": entry["meaning"],
        "example": entry["example"],
        "language": lang
    })


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
