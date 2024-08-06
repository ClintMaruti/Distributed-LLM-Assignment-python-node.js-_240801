from flask import Flask, request, jsonify, session
from models.llama2_model import LlamaModel
from models.mistral_model import MistralModel
from flask_session import Session
from dotenv import load_dotenv
import uuid
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Session configuration
app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE')  # Set session type from environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Set secret key from environment variable
Session(app)  # Initialize session management

# Model instances
mistral_model = MistralModel()  # Create an instance of the Mistral model
llama_model = LlamaModel()  # Create an instance of the Llama2 model

def select_model(model):
    data = request.get_json()  # Get JSON data from the request
    model = data.get('model')  # Get the model name from the request data

    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4()

    if model == 'Llama2':
        session['model'] = 'Llama2'  # Set session model to Llama2
    
    elif model == 'Mistral':
        session['model'] = 'Mistral'  # Set session model to Mistral
    
    else:
        return {'model': '', "session_id": ''} # Return error if invalid model is selected

@app.route('/')
def index():
    return 'Health 100%'  # Health check endpoint

@app.route('/get_session')
def get_session():
    message = session.get('model', 'No session data found')  # Retrieve model information from session
    return f'Session data: {message}'  # Return session data

@app.route('/chat', methods=['POST'])
def query():
    data = request.get_json()  # Get JSON data from the request
    query = data.get('query')  # Get the query from the request data
    model = data.get('model') # Get the model from the request data
    
    if not query:
        return jsonify({"error": "Query not provided"}), 400  # Return error if query is not provided
    
    if not model:
        return jsonify({"error": "Model not provided"}), 400  # Return error if model is not provided
    
    # set model in session and create session_id
    select_model(model)

    model = session['model']  # Get the model from session data

    curr_session = session['session_id'] # Get the current session ID from session data

    if model == 'Llama2':
        response = llama_model.chatbot(query, curr_session)  # Use Llama2 model to get the response
    elif model == 'Mistral':
        response = mistral_model.chatbot(query, curr_session)  # Use Mistral model to get the response
    else:
        return jsonify({"error": "Invalid model in session"}), 400  # Return error if invalid model in session

    return jsonify({"response": response})  # Return the response from the model

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode