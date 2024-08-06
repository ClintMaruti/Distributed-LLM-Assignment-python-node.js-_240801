import os
from llamaapi import LlamaAPI
from dotenv import load_dotenv

# Load .env file
load_dotenv()

LLAMA_API_KEY = os.getenv('LLAMA_API_KEY') 

class LlamaModel:
    def __init__(self) -> None:
        # Initialize the LlamaModel class with a client and an empty chat history
        self.client = LlamaAPI(LLAMA_API_KEY)  # Instantiate the API client with the provided API key
        self.chat_history = {}  # Dictionary to store chat history for different sessions

    def construct_chat_history(self, user, assistant, session_id):
        """
        Constructs and updates the chat history string from assistant and user messages.

        Parameters:
        - user (dict): A dictionary with 'role' and 'content' for the user message.
        - assistant (dict): A dictionary with 'role' and 'content' for the assistant message.
        - session_id (str): The identifier for the chat session.

        Returns:
        - str: The updated chat history for the given session.
        """
        # Validate input
        if not isinstance(assistant, dict) or not isinstance(user, dict):
            raise ValueError("Both parameters must be dictionaries.")
        
        if 'role' not in assistant or 'content' not in assistant:
            raise ValueError("Assistant message must contain 'role' and 'content'.")
        
        if 'role' not in user or 'content' not in user:
            raise ValueError("User message must contain 'role' and 'content'.")
        
        if session_id == None:
            raise ValueError("Session id must be provided")

        # Extract role and content
        assistant_content = assistant.get('content', '')
        user_content = user.get('content', '')

        # Initialize chat history for a new session if it does not exist
        if session_id not in self.chat_history:
            self.chat_history[session_id] = ""

        # Append new messages to the existing chat history
        self.chat_history[session_id] += f"User: {user_content}\nAssistant: {assistant_content}\n"
        
        return self.chat_history[session_id]
        
    def contextualize_query(self, chat_history, user_query):
            """
            Generates a contextualized stand-alone query based on the provided chat history and user query.

            Parameters:
            - chat_history (str): The formatted chat history as a string.
            - user_query (str): The user's query to be contextualized.

            Returns:
            - str: The contextualized stand-alone query.
            """
            # Prepare the API request JSON for contextualizing the query
            api_request_json = {
                "model": "llama3-70b", 
                "messages": [
                    {"role": "system", "content": "You are an intelligent chat-bot. Contextualize the following user query based on the provided chat history."},
                    {"role": "system", "content": f"Chat history: {chat_history}"},
                    {"role": "user", "content": f"User query: {user_query}"}
                ]
            }

            # Send the request to the Llama API
            response = self.client.run(api_request_json)

            # Extract the contextualized query from the API response
            contextualized_query = response.json()['choices'][0]['message']['content']

            return contextualized_query
    
    def chatbot(self, query, session_id):
        """
        Processes a user query using the Llama API and updates the chat history.

        Parameters:
        - query (str): The user's query.
        - session_id (str): The identifier for the chat session.

        Returns:
        - str: The assistant's response to the query.
        """
        # Construct the user message for the API request
        user_message = {'role': 'user', 'content': query}

        # Initialize chat history for a new session if it does not exist
        if session_id not in self.chat_history:
            self.chat_history[session_id] = ""

        # Generate a contextualized query based on the updated chat history
        contextualized_query = self.contextualize_query(self.chat_history[session_id], query)
        
        # Prepare the API request JSON
        api_request_json = {
            "model": "llama3-70b",  # Specify the model to use
            "messages": [
                {"role": "system", "content": "You are an intelligent chat-bot. Answer the following questions according to your knowledge."},
                {"role": "user", "content": contextualized_query},  # Use the contextualized query
            ]
        }

        # Send the request to the Llama API
        response = self.client.run(api_request_json)

        # Extract the assistant's response from the API response
        ass_message = response.json()['choices'][0]['message']

        # Update the chat history with the user and assistant's response
        self.construct_chat_history(user_message, ass_message, session_id)

        return ass_message
