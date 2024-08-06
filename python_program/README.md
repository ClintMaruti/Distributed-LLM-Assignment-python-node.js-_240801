---
# Llama2 and Mistral API

This project provides a Flask-based API to interact with Llama2 and Mistral language models. It allows users to select a model, send queries, and maintain conversation context between interactions.

## Features

- **Model Selection**: Choose between Llama2 and Mistral models.
- **Querying**: Send text queries to the selected model.
- **Context Maintenance**: The API maintains conversation context between queries.

## Prerequisites

- Python 3.8 or later
- A compatible GPU (recommended for running large models)
- CUDA and cuDNN for GPU acceleration (if using a GPU)

## Installation

1. **Clone the Repository**

   ```bash
   git clone git@github.com:ClintMaruti/Distributed-LLM-Assignment-python-node.js-_240801.git
   cd Distributed-LLM-Assignment-python-node.js-_240801

2. **Create a Virtual Environment**

   ```sh
   python3 -m venv llm-env
   source llm-env/bin/activate  # On Windows use `llm-env\Scripts\activate`
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project with the following content:

   ```env
   SECRET_KEY=your_secret_key
   SESSION_TYPE=filesystem
   MISTRAL_API_KEY=----
   LLAMA_API_KEY=---
   ```

   Replace `your_secret_key` with a secure secret key.
   Replace `MISTRAL_API_KEY` and `LLAMA_API_KEY` with their your own.

   OR...

   Simply rename `.env.example` file to `.env` to use mine

5. **Install Model Dependencies**

   If necessary, install additional dependencies for model support:

   ```sh
   pip install torch transformers
   ```

## Running the Application

1. **Start the Flask Application**

   ```sh
   export FLASK_APP=app.py
   flask run
   ```

   On Windows, use:

   ```sh
   set FLASK_APP=app.py
   flask run
   ```

2. **Access the API**

   The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Select Model

- **Endpoint**: `/select_model`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "model": "Llama2" // or "Mistral"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Llama2 model selected"
  }
  ```

### Query

- **Endpoint**: `/query`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "query": "Your question here"
  }
  ```
- **Response**:
  ```json
  {
    "response": "Model's response here"
  }
  ```

## Contributing

1. **Fork the Repository**: Create a personal copy of the repository on GitHub.
2. **Clone Your Fork**: Clone the repository to your local machine.
3. **Create a Branch**: Create a new branch for your changes.
4. **Commit Changes**: Commit your changes with descriptive messages.
5. **Push Changes**: Push your changes to your forked repository.
6. **Create a Pull Request**: Submit a pull request to merge your changes into the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](git@github.com:ClintMaruti/Distributed-LLM-Assignment-python-node.js-_240801.git).
---
