---

# Chat Application

A Node.js application for handling chat interactions, storing conversation histories, and integrating with external chat models. This application uses Express, Firebase, and a custom chat model API.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [License](#license)

## Installation

1. **Clone the Repository**

   ```bash
   git clone git@github.com:ClintMaruti/Distributed-LLM-Assignment-python-node.js-_240801.git
   cd Distributed-LLM-Assignment-python-node.js-_240801

2. **Install Dependencies**

   Ensure you have Node.js and npm installed. Install the project dependencies:

   ```bash
   npm install
   ```

3. **Setup Environment Variables**

   Create a `.env` file in the root directory and add the following environment variables:

   ```env
   BASE_URL=http://127.0.0.1:5000
   PORT=3000
   ```

   Replace `your_chat_model_api_base_url` with the actual base URL of your chat model API.

4. **Setup Firebase**

   Ensure you have Firebase set up and configure your `firebaseConfig` file with your Firebase project details.

## Configuration

The project uses environment variables for configuration. Ensure that your `.env` file is correctly set up as described in the Installation section.

## Usage

1. **Start the Server**

   ```bash
   npm start
   ```

   The server will start on the port specified in your `.env` file (default is 3000).

2. **Access the API**

   - **Health Check**: `GET /` - Returns a health check message.
   - **Send Chat**: `POST /chat` - Sends a chat query to the model and stores the conversation.
     - Request body:
       ```json
       {
         "model": "Mistral",
         "query": "Hello",
         "user_email": "test@example.com"
       }
       ```
   - **Conversation History**: `GET /conversation-history` - Retrieves all conversations from the database.
   - **User Conversation History**: `GET /conversation-history/:email` - Retrieves conversation history for a specific user.

## Testing

1. **Run Tests**

   Ensure all dependencies are installed and run the tests using:

   ```bash
   npm test
   ```

   This will execute Jest tests and report any issues.

2. **Add Tests**

   - **API Tests**: Located in `src/__tests__/routes.test.ts`
   - **Function Tests**: Located in `src/__tests__/api.test.ts` and `src/__tests__/repo.test.ts`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
