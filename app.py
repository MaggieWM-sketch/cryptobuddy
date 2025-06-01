from flask import Flask, render_template, request
from crypto_chatbot import analyze_crypto, personalized_insights

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get("msg")
    response = analyze_crypto(user_text) if user_text else "Ask me about crypto trends!"
    return str(response)

@app.route("/personalized")
def personalized_advice():
    risk_level = request.args.get("risk")
    investment_goal = request.args.get("goal")
    sustainability_preference = request.args.get("sustainable")
    response = personalized_insights(risk_level, investment_goal, sustainability_preference)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
