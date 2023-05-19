from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openai
import json
#langchain imports
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts.chat import HumanMessagePromptTemplate, ChatPromptTemplate

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

with open('openai_api.txt', 'r') as file:
    openai_key = file.read().strip()

openai.api_key = openai_key

# Load the prompts.json file into a Python dictionary
with open('prompts.json', 'r') as f:
    prompts = json.load(f)

# Convert the list of prompts into a dictionary
prompts_dict = {prompt['question_number']: prompt['system'] for prompt in prompts}


llm = ChatOpenAI(temperature=0.1, openai_api_key=openai_key)
global messages
messages = []

@app.route('/save_message', methods=['POST'])
def save_message():
    global messages
    data = request.get_json()
    question = data['question']
    answer = data['answer']  # Assuming 'answer' is now part of the request to this endpoint
    user_response = UserResponse(question=question, answer=answer, conversation=json.dumps(messages))
    db.session.add(user_response)
    db.session.commit()
    messages = []

    return 'Response saved'

@app.route('/chat', methods=['POST'])
def chat():
    global messages
    data = request.get_json()
    message = data['message']
    question_number = data['questionNumber'] + 1
    system_message_content = prompts_dict[question_number]

    # Add the system message and user's message to the conversation
    system_message = SystemMessage(content=system_message_content)
    user_message = HumanMessage(content=message)
    messages_temp = [system_message, user_message]

    # Call GPT-3.5 and get the response
    response = llm(messages_temp)
    messages.append([message, response.content])

    # Return the chatbot's response
    return response.content


def summarize_conversation(conversation, llm):
    prompt = """Please summarize the following conversation with a focus on vitamins intake, meal behaviours and anything regarding tailoring a vitamin to a specific user needs: {input}"""
    human_template = HumanMessagePromptTemplate.from_template(template=prompt)
    chat_prompt = ChatPromptTemplate.from_messages([human_template])
    chat_prompt_value = chat_prompt.format_prompt(input=conversation)
    summary = llm([chat_prompt_value.to_messages()[0]])
    return summary.content


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
    # Generate a single string that contains the whole conversation
    entire_conversation = " ".join([conv['chatbot_conversation'] for conv in response])
    
    # Call the summarization function
    summary = summarize_conversation(entire_conversation, llm)

    response.append({
        'conversation_summary': summary, 
        'discrepancies': 'TODO'  #TODO do this with the detected discrepancies fetched from OpenAI's API
    })
    return json.dumps(response)

@app.route('/summary')
def summary():
    return render_template('summary.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
