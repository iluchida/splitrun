from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
import os, csv, json, uuid, hashlib, time, requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key")

# Flask-Session設定の追加（app.py の Session(app) の前に）
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(os.getcwd(), "flask_session")
app.config["SESSION_PERMANENT"] = False

# ここを明示！
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # または "None", "Strict"
app.config["SESSION_COOKIE_SECURE"] = False    # HTTPSでなければFalseに
Session(app)


# Gemini REST API設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# 定数
# CACHE_FILE = "data/cache.json"
# CSV_FILE = "private_data/responses.csv"
# NGWORD_FILE = "private_data/ngwords.csv"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "private_data")
CACHE_FILE = os.path.join(BASE_DIR, "data", "cache.json")
CSV_FILE = os.path.join(DATA_DIR, "responses.csv")
NGWORD_FILE = os.path.join(DATA_DIR, "ngwords.csv")

os.makedirs(DATA_DIR, exist_ok=True)

QUESTIONS = {
    "design": "ユーザー体験を向上させるために、どのようなデザイン思考を導入すべきですか？",
    "creative": "効果的な広告クリエイティブを制作するには、どのような要素を意識すべきですか？",
    "distribution": "広告配信先を選定する際、どのようなデータや指標をもとに意思決定するのが良いですか？",
    "validation": "ペルソナ設計や顧客インサイトを抽出するために、どのような検証プロセスが有効でしょうか？",
    "competitive": "自社サービスの市場優位性を、競合と比較してどのようにアピールすべきだと考えますか？"
}

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

cache = load_cache()

def load_ngwords():
    ngwords = {}
    if os.path.exists(NGWORD_FILE):
        with open(NGWORD_FILE, encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    key = row[0].strip()
                    words = [w.strip() for w in row[1:] if w.strip()]
                    ngwords[key] = words
    return ngwords

NGWORDS = load_ngwords()

def contains_ngword(question_key, user_input):
    ng_list = NGWORDS.get(question_key, [])
    return any(ng in user_input for ng in ng_list)

def get_jst_timestamp():
    return (datetime.utcnow() + timedelta(hours=9)).strftime("%Y/%m/%d %H:%M:%S")

def generate_answer(question, user_input, retries=3, delay=5):
    key = hashlib.md5((question + user_input).encode("utf-8")).hexdigest()
    if key in cache:
        return cache[key]

    prompt = f"{question}\n\n入力内容: {user_input}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    for attempt in range(retries):
        try:
            res = requests.post(GEMINI_API_URL, headers=headers, json=data)
            res.raise_for_status()
            answer = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            cache[key] = answer
            save_cache(cache)
            return answer
        except Exception as e:
            print(f"[Gemini Retry {attempt + 1}] {e}")
            time.sleep(delay)
    return "AI回答の取得に失敗しました。"

@app.route("/")
def index():
    form_data = session.pop("form_data", {})
    errors = session.pop("errors", {})
    return render_template("form.html", data=form_data, errors=errors)

@app.route("/confirm", methods=["POST"])
def confirm():
    form_data = {}
    ai_answers = {}
    errors = {}

    for key in QUESTIONS.keys():
        user_input = request.form.get(key, "").strip()
        ai_answer = request.form.get(f"ai_{key}", "").strip()
        form_data[key] = user_input
        ai_answers[f"ai_{key}"] = ai_answer
        if not user_input:
            errors[key] = "この項目は必須です"

    if errors:
        session["form_data"] = form_data
        session["errors"] = errors
        return redirect(url_for("index"))

    session["form_data"] = form_data
    session["ai_answers"] = ai_answers
    return render_template("confirm.html", data=form_data, ai_answers=ai_answers, questions=QUESTIONS)


@app.route("/submit", methods=["POST"])
def submit():
    form_data = session.pop("form_data", None)
    ai_answers = session.pop("ai_answers", None)

    if not form_data or not ai_answers:
        print("[ERROR] フォームデータまたはAI回答が空です")
        return redirect(url_for("index"))

    try:
        os.makedirs("private_data", exist_ok=True)
        is_new = not os.path.exists(CSV_FILE)
        with open(CSV_FILE, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["UUID", "日時", "設問キー", "ユーザー入力", "AI回答"])
            now = get_jst_timestamp()
            uid = str(uuid.uuid4())
            for key, user_input in form_data.items():
                ai_ans = ai_answers.get(key, "")
                writer.writerow([uid, now, key, user_input, ai_ans])
        print(f"[OK] CSVに保存完了（ID: {uid}）")
    except Exception as e:
        print("[ERROR] CSV保存失敗:", e)

    return render_template("result.html", results=ai_answers, questions=QUESTIONS)

@app.route("/ai-response", methods=["POST"])
def ai_response():
    try:
        data = request.get_json()
        question_key = data.get("question_key")  # ← JavaScriptと一致
        user_input = data.get("user_input")

        if not question_key or not user_input:
            return jsonify({"error": "入力が不正です"}), 400

        question = QUESTIONS.get(question_key)
        if not question:
            return jsonify({"error": f"設問キー「{question_key}」が無効です"}), 400

        if contains_ngword(question_key, user_input):
            return jsonify({"answer": "NGワードが含まれているため、回答できません。"})

        answer = generate_answer(question, user_input)
        return jsonify({"answer": answer})
    except Exception as e:
        import traceback
        print("[ERROR] /ai-response:", e)
        traceback.print_exc()
        return jsonify({"error": "AI回答の取得に失敗しました。"}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
