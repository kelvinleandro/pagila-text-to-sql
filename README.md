# 💬 Chat with Your Data (Pagila Database)

This project allows users to interact with a PostgreSQL database by asking questions. It leverages a Large Language Model (LLM) to translate natural language queries into SQL, execute them, and return human-readable answers.

The entire application is containerized using Docker, making it easy to set up and run with a single command.

## 🏛️ Project Architecture

The application is built on a modern, decoupled architecture consisting of three main services orchestrated by Docker Compose:

1. **Database** (db): A PostgreSQL container running the [**Pagila**](https://github.com/devrimgunduz/pagila) sample database. It is pre-configured with a read-only user for the backend to ensure data safety.

2. **Backend** (backend): A **FastAPI** application that serves a single API endpoint (`/api/query`). It contains the core logic, using a **LangChain SQL Agent** to:

   - Inspect the database schema.

   - Generate SQL queries from user questions using an OpenAI LLM.

   - Execute the query against the database.

   - Synthesize a natural language response from the query results.

3. **Frontend** (frontend): A **Streamlit** web application that provides a simple and interactive chat interface for the user. It communicates with the backend's API to send questions and display answers.

All services run on a shared Docker network, allowing them to communicate seamlessly using their service names.

## ✨ Features

- **Natural Language Querying**: Ask complex questions like "Who are the top 5 customers by total spending?"

- **Secure by Design**: The backend connects to the database using a read-only user, preventing any possibility of data modification or deletion.

- **Scalable Backend**: Built with FastAPI, the backend is asynchronous and ready for high performance.

- **Interactive UI**: A clean and simple user interface built with Streamlit.

- **Fully Containerized**: The entire stack is managed with Docker and Docker Compose for easy, one-command setup and deployment.

## 💻 Tech Stack

- **Backend**: Python, FastAPI, LangChain, OpenAI, SQLAlchemy

- **Frontend**: Python, Streamlit, Requests

- **Database**: PostgreSQL (with the Pagila sample dataset)

- **DevOps**: Docker, Docker Compose

## 🚀 Getting Started

Follow these steps to get the entire application running on your local machine.

### Prerequisites

- Docker and Docker Compose must be installed on your system.

- An OpenAI API Key.

### 1. Clone the Repository

```bash
git clone https://github.com/kelvinleandro/pagila-text-to-sql.git
cd pagila-text-to-sql
```

### 2. Create the Environment File

The application uses separate `.env` files for the backend and frontend. In both the `backend/` and `frontend/` directories, you will find a `.env.example` file. Make a copy of each and rename them to `.env`, then fill in your credentials.

> **Important**: When running with Docker, ensure the variables in your new `.env` files point to the correct service names (e.g., `db` for the database hostname and `http://backend:8000/api` for the API URL) and not `localhost`.

### 3. Build and Run the Application

With Docker running, execute the following command from the project root:

```bash
docker compose up --build
```

To run the containers in the background (detached mode), use:

```bash
docker compose up --build -d
```

### 4. Access the Services

Once everything is running, you can access the application:

- **Streamlit Frontend**: Open your web browser and go to http://localhost:8501

- **FastAPI Backend Docs**: To see the API documentation, go to http://localhost:8000/docs

## 🔧 How to Use

1. Navigate to http://localhost:8501.

2. Type a question about the Pagila DVD rental database into the text input box.

3. Click the send button.

4. The answer will appear below.

### Example Questions:

- "What are the 5 longest movies? Show me their titles and lengths."

- "Show me the total revenue for each store."

- "Which 3 actors have appeared in the most films?"

- "How many films are in the 'Action' category?"

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
