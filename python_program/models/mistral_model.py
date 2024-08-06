import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

class MistralModel:
    def __init__(self) -> None:
        # Initialize the model name and API client
        self.model_name = 'mistral-large-latest'
        self.client = MistralClient(api_key)
        # Initialize chat history storage
        self.chat_history = {}

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
        # Validate input types and required keys
        if not isinstance(assistant, dict) or not isinstance(user, dict):
            raise ValueError("Both parameters must be dictionaries.")
        
        if 'role' not in assistant or 'content' not in assistant:
            raise ValueError("Assistant message must contain 'role' and 'content'.")
        
        if 'role' not in user or 'content' not in user:
            raise ValueError("User message must contain 'role' and 'content'.")
        
        if session_id is None:
            raise ValueError("Session id must be provided")

        # Extract message content
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

        # Prepare messages to be sent to the API for contextualizing the query
        message_construct = [
            ChatMessage(role="system", content="Based on the provided Chat history and the User query, formulate a stand-alone query. If the chat history is empty, return the user query as it is."),
            ChatMessage(role="system", content=f"Chat history: {chat_history}"),
            ChatMessage(role="user", content=f"User query: {user_query}"),
        ]
        
        # Send the request to the Mistral API
        response = self.client.chat(model=self.model_name, messages=message_construct)

        # Extract the contextualized query from the API response
        contextualized_query = response.choices[0].message.content

        return contextualized_query

    def chatbot(self, query, session_id):
        """
        Processes a user query using the Mistral API and updates the chat history.

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

        # Send the contextualized query to the Mistral API
        response = self.client.chat(model=self.model_name, messages=[ChatMessage(role="user", content=contextualized_query)])

        # Extract the assistant's response from the API response
        ass_message = {'role': 'assistant', 'content': response.choices[0].message.content}

        # Update the chat history with the user and assistant's response
        self.construct_chat_history(user_message, ass_message, session_id)

        return response.choices[0].message.content
