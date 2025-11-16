import json
import glob
from langdetect import detect

IDIOM_DATA_FOLDER = "gemma"   # folder with JSON idioms

idiom_dict = {}

print("\n🔍 Loading idiom files...\n")

# ----------------------------------------------------
# LOAD IDIOM DATA
# ----------------------------------------------------
for file in glob.glob(f"{IDIOM_DATA_FOLDER}/*.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                print(f"⚠ Invalid JSON list skipped: {file}")
                continue

            for entry in data:
                idiom = entry.get("idiom", "").strip().lower()

                literal = entry.get("literal_meaning", "").strip()
                figurative = entry.get("figurative_meaning", "").strip()
                example = entry.get("example", "").strip()

                if idiom:
                    idiom_dict[idiom] = {
                        "literal": literal,
                        "meaning": figurative,
                        "example": example
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
# IDIOM MATCHING
# ----------------------------------------------------
def find_idiom(sentence):
    s = sentence.lower()
    for idiom in idiom_dict.keys():
        if idiom in s:
            return idiom
    return None


# ----------------------------------------------------
# HIGHLIGHT IDIOM INSIDE SENTENCE
# ----------------------------------------------------
def highlight(sentence, idiom):
    idiom_lower = idiom.lower()
    return sentence.replace(
        idiom,
        f"**{idiom}**"
    ).replace(
        idiom.capitalize(),
        f"**{idiom.capitalize()}**"
    )


# ----------------------------------------------------
# MAIN ANALYSIS
# ----------------------------------------------------
def analyze_sentence(sentence):

    idiom = find_idiom(sentence)
    lang = detect_language(sentence)

    if not idiom:
        return "\n❌ No idiom found.\n"

    entry = idiom_dict[idiom]

    highlighted = highlight(sentence, idiom)

    return (
        f"\n🟢 **Idiom Detected:** `{idiom}`\n\n"
        f"📌 **Your sentence:**\n{highlighted}\n\n"
        f"💡 **Literal Meaning:**\n{entry['literal']}\n\n"
        f"✨ **Figurative Meaning:**\n{entry['meaning']}\n\n"
        f"📝 **Example Usage:**\n{entry['example']}\n\n"
        f"🌐 **Language Detected:** {lang}\n"
    )


# ----------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------
if __name__ == "__main__":
    print("\n🔍 Multilingual Idiom Detector — Enhanced Version\n")

    while True:
        text = input("Enter sentence: ")

        if text.lower().strip() == "exit":
            break

        print(analyze_sentence(text))
        print("---------------------------------------")
