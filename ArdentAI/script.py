from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

# Simple memory
memory = {}

# Predefined responses
greetings = ["hello", "hi", "hey", "good morning", "good evening"]
how_are_you = ["how are you", "how is it going"]

@app.route("/")
def home():
    return "Big Mind AI Server is Running! Use POST /ai"

@app.route("/ai", methods=["POST"])
def ai():
    data = request.json or {}
    text = data.get("text", "").lower().strip()
    reply = "I am not sure how to answer that."

    # Check memory first
    if text in memory:
        return jsonify({"reply": memory[text]})

    # Greetings
    if any(word in text for word in greetings):
        reply = "Hello! I am your Big Mind AI assistant."
    elif any(word in text for word in how_are_you):
        reply = "I am always ready to help! 😎"

    # Math solving
    elif any(op in text for op in ["+", "-", "*", "/", "**", "sqrt", "pow"]):
        try:
            # Safe replacements for sqrt, pow
            safe_text = text.replace("sqrt", "math.sqrt").replace("pow", "math.pow")
            # Allow only numbers, operators, math functions
            allowed_chars = "0123456789+-*/(). "
            expr = "".join([c for c in safe_text if c.isalnum() or c in "+-*/(). "])
            result = eval(expr, {"__builtins__": None, "math": math})
            reply = f"Answer is {result}"
        except:
            reply = "I could not solve that math problem."

    # Learn new things
    elif text.startswith("remember:"):
        try:
            # Format: remember: question = answer
            parts = text[9:].split("=")
            question = parts[0].strip()
            answer = parts[1].strip()
            memory[question] = answer
            reply = f"I remembered that '{question}' = '{answer}'"
        except:
            reply = "Failed to remember. Use format: remember: question = answer"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

