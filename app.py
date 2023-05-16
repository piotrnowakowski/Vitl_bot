from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openai
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
import openai
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite database 'site.db'
db = SQLAlchemy(app)

class UserResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    conversation = db.Column(db.String(500), nullable=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/save_message', methods=['POST'])
def save_message():
    data = request.get_json()
    user_response = UserResponse(question=data['question'], answer=data['answer'])
    db.session.add(user_response)
    db.session.commit()
    return 'Response saved'

with open('openai_api.txt', 'r') as file:
    openai_key = file.read().strip()

openai.api_key = openai_key

with open('prompts.json') as f:
    prompts = json.load(f)

# Initialize a ConversationChain with ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=3)
llm = OpenAI(temperature=0.5, openai_api_key=openai_key)
chain = ConversationChain(llm=llm, memory=memory)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    question_number = data['questionNumber']

    # Call GPT-3.5 and get the response
    response = chain.predict(input=message)

    # Save the user's message and the chatbot's response in the database
    user_response = UserResponse(question=prompts[question_number]['system'], answer=message, conversation=json.dumps(chain.memory.load_memory_variables({})))
    db.session.add(user_response)
    db.session.commit()

    # Return the chatbot's response
    return response

@app.route('/get_conversation', methods=['GET'])
def get_conversation():
    all_conversations = UserResponse.query.all()
    response = []
    for conversation in all_conversations:
        response.append({
            'id': conversation.id,
            'question': conversation.question,
            'answer': conversation.answer,
            'chatbot_conversation': conversation.conversation
        })
    # Fetch conversation summary and detected discrepancies from OpenAI's API here
    # and append them to the response
    response.append({
        'conversation_summary': 'TODO',  # Replace 'TODO' with the conversation summary fetched from OpenAI's API
        'discrepancies': 'TODO'  # Replace 'TODO' with the detected discrepancies fetched from OpenAI's API
    })
    return json.dumps(response)

@app.route('/summary')
def summary():
    return render_template('summary.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
