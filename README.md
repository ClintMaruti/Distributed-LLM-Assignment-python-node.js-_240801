---

# Distributed LLM Assignment (python, node.js)_240801

This project consists of two main components: a Node.js Express application and a Python Flask application. These applications are designed to work together, with the Node.js app interacting with the Flask app. Both applications are containerized using Docker and managed with Docker Compose.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [License](#license)

## Project Structure

The project is organized into two main directories:

- `node_express_program`: Contains the Node.js Express application.
- `python_program`: Contains the Python Flask application.
- `docker-compose.yml`: Docker Compose configuration file to manage both applications.

## Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Steps

1. **Clone the Repository**

   ```bash
   git clone git@github.com:ClintMaruti/Distributed-LLM-Assignment-python-node.js-_240801.git
   cd Distributed-LLM-Assignment-python-node.js-_240801
   ```

2. **Build and Start the Containers**

   Navigate to the root directory (parent directory) and run:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images for both the Node.js and Python applications and start the containers.

## Configuration

### Environment Variables

Create a `.env` file in the root directory of each sub-project (`node_express_program` and `python_program`) and add the necessary environment variables.

#### Node.js Express Application

```env
# node_express_program/.env
BASE_URL=http://python_program:5000
PORT=3000
```

#### Python Flask Application

```env
# python_program/.env
SECRET_KEY=hyperhire
SESSION_TYPE=filesystem
MISTRAL_API_KEY=hcNgC8pWqzie9Jg8ePNdWvPWorAWMH4t
LLAMA_API_KEY=LL-dKQB8SMXjhGZh1e7sBYpuoee0cMj68peWev3xUFwdK43WaVtxIKGE9CfcwwNhm8w
```

## Usage

### Accessing the Applications

- **Node.js Express Application**: Accessible at `http://localhost:3000`
- **Python Flask Application**: Accessible at `http://localhost:5000`

### API Endpoints

#### Node.js Express Application

- **Health Check**: `GET /`
  - Returns a health check message.
  
- **Send Chat**: `POST /chat`
  - Sends a chat query to the model and stores the conversation.
  - Request body:
    ```json
    {
      "model": "Mistral",
      "query": "Hello",
      "user_email": "test@example.com"
    }
    ```

- **Conversation History**: `GET /conversation-history`
  - Retrieves all conversations from the database.

- **User Conversation History**: `GET /conversation-history/:email`
  - Retrieves conversation history for a specific user.

#### Python Flask Application

- **Health Check**: `GET /`
  - Returns a health check message.

- **Get Session**: `GET /get_session`
  - Retrieves the current session data.

- **Chat**: `POST /chat`
  - Sends a chat query to the selected model.
  - Request body:
    ```json
    {
      "query": "Hello",
      "model": "Llama2"
    }
    ```
  - Response:
    ```json
    {
      "response": "Hello! How can I assist you today?"
    }
    ```

## Testing

### Node.js Express Application

1. **Install Development Dependencies**

   ```bash
   cd node_express_program
   npm install --only=dev
   ```

2. **Run Tests**

   ```bash
   npm test
   ```

### Python Flask Application

1. **Install Development Dependencies**

   ```bash
   cd python_program
   pip install -r requirements.txt
   ```

2. **Run Tests**

   Ensure you have a testing framework set up (e.g., `pytest`) and run your tests accordingly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
