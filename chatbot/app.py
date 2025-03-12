import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the intent data from Intent.json
with open('./Intent.json', 'r') as file:
    intents = json.load(file)

def find_best_intent(user_question):
    user_question = user_question.lower()  # Convert input to lowercase
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_question:  # Case-insensitive substring match
                return intent['intent_tag'], intent['responses'][0]  # Return first response
    return None, "I'm sorry, I couldn't understand your question."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_intent', methods=['POST'])
def get_intent():
    user_question = request.json.get('user_question', "")

    # Find the matching intent
    intent_tag, response = find_best_intent(user_question)

    return jsonify({
        "intent_tag": intent_tag,
        "response": response,
        "user_question": user_question
    })

if __name__ == '__main__':
    app.run(debug=True)
