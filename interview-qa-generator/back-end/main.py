from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from prompt_builder import build_prompt
from gemini_client import get_llm_response as get_gemini_response
from question_parser import parse_qa

app = Flask(__name__)
app.secret_key = "your_secret_key"
CORS(app, supports_credentials=True)

users = {}  # For demo only. Use a database in production!

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"success": False, "error": "Email and password required"})
    if email in users:
        return jsonify({"success": False, "error": "User already exists"})
    users[email] = generate_password_hash(password)
    session["user"] = email
    return jsonify({"success": True})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if email not in users or not check_password_hash(users[email], password):
        return jsonify({"success": False, "error": "Invalid credentials"})
    session["user"] = email
    return jsonify({"success": True})

@app.route('/api/generate', methods=['POST'])
def generate():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    role = data.get("role")
    tools = data.get("tools", [])
    experience = data.get("experience", "")
    count = int(data.get("count", 5))

    if not role:
        return jsonify({"error": "Missing job role"}), 400

    prompt = build_prompt(role, tools, experience, count)
    raw_output = get_gemini_response(prompt)
    print("Gemini raw output:", raw_output)

    # Parse and sanitize
    all_qas = parse_qa(raw_output)

    print(f"Parsed {len(all_qas)} questions.")
    for i, qa in enumerate(all_qas):
        print(f"Q{i+1}: {qa.get('question')}")

     # 🧪 BONUS TIP: Preview the first valid parsed result
    if all_qas:
        print("🧪 Bonus Tip - First Parsed QA:", all_qas[0])

    # Ensure it's a list of dicts with required keys
    filtered_qas = []
    for qa in all_qas:
        if all(k in qa for k in ("question", "answer", "critique")):
            # Strip weird formatting from answers
            for k in qa:
                if isinstance(qa[k], str):
                    qa[k] = qa[k].replace("<br>", "").replace("**", "").replace("__", "").strip()
            filtered_qas.append(qa)
        if len(filtered_qas) >= count:
            break

    if len(filtered_qas) < count:
        print(f"Warning: Only {len(filtered_qas)} out of {count} questions generated.")

    return jsonify({"result": filtered_qas})

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate_alias():
    if request.method == 'OPTIONS':
        return '', 204
    return generate()

@app.route('/', methods=['GET'])
def home():
    return "Interview Ques-Ans Generator API is running!"

@app.route('/api/generate/api', methods=['GET'])
def generate_api():
    prompt = build_prompt("Software Engineer", ["Python"], "Fresher", 5)
    ai_response = {
        "prompt": prompt,
        "response": f"GenAI says: '{prompt[::-1]}'"
    }
    return jsonify(ai_response)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)