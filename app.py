from flask import Flask, request, render_template, jsonify
import os
import requests

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一位营养专家AI助手，擅长提供科学、实用的饮食建议和营养方案。"},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://api.deepseek.com/v1/chat/completions",
                             headers=headers, json=payload)

    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
