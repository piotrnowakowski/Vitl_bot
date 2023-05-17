from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openai
import json
#langchain imports
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


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

# Load the prompts.json file into a Python dictionary
with open('prompts.json', 'r') as f:
    prompts = json.load(f)

# Convert the list of prompts into a dictionary
prompts_dict = {prompt['question_number']: prompt['system'] for prompt in prompts}


# Initialize a ConversationChain with ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=3)
llm = ChatOpenAI(temperature=0.1, openai_api_key=openai_key)
chain = ConversationChain(llm=llm, memory=memory)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    question_number = data['questionNumber'] + 1
    system_message_content = prompts_dict[question_number]

    # Add the system message and user's message to the conversation
    system_message = SystemMessage(content=system_message_content)
    user_message = HumanMessage(content=message)
    messages = [system_message, user_message]

    # Call GPT-3.5 and get the response
    response = llm(messages)

    # Save the user's message, the chatbot's response and the entire conversation in the database
    conversation = [{'role': msg.role, 'content': msg.content} for msg in chain.memory.load_memory_variables({}).get('messages', [])]
    user_response = UserResponse(question=system_message_content, answer=message, conversation=json.dumps(conversation))
    db.session.add(user_response)
    db.session.commit()

    # Return the chatbot's response
    return response.content


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
