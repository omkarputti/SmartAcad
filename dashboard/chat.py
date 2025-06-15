from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyDEbcGzKj7riZXozkJdx9_yHUml9UnzE_c")

model = genai.GenerativeModel('gemini-pro')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    response = model.generate_content(user_input)
    return jsonify({"reply": response.text})

if __name__ == '_main_':
    app.run(debug=True)