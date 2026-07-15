# Habit Builder Bot 🚀

Welcome to the **Habit Builder Bot**—your personal, AI-powered habit and accountability coach. This application consists of a robust **FastAPI backend** running a LangGraph agent powered by Gemini or Groq, paired with an interactive **Streamlit frontend** UI.

---

## 🛠️ Prerequisites

Before getting started, make sure you have [uv](https://github.com/astral-sh/uv) installed on your system. `uv` is used for ultra-fast dependency management and virtual environment handling.

---

## ⚙️ Setup Instructions

Follow these steps to get the application set up locally:

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd habit-builder-bot

```

### 2. Install Dependencies

Use `uv` to automatically create a virtual environment and sync all required packages:

```bash
uv sync

```

### 3. Configure Environment Variables

Create a `.env` file in the root directory of the project. You can copy the template from `.env.example`:

```bash
cp .env.example .env

```

Open `.env` and fill in your model configuration and API keys:

```text
# Use the provider prefix (e.g., groq:model_name or google_genai:model_name)
MODEL_NAME=groq:llama-3.3-70b-versatile

# Add your relevant API keys
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here

```

---

## 🚀 Running the Application

To run the application, you must start the backend server **first**, followed by the frontend interface.

### Step 1: Start the FastAPI Backend (First)

The backend initializes the SQLite database tables on startup and runs the AI agent. Run this in your first terminal:

```bash
uv run uvicorn main:app --reload

```

*The backend will be available at `[http://127.0.0.1:8000](http://127.0.0.1:8000)`.*

### Step 2: Start the Streamlit Frontend (Second)

Once the backend is up and running, open a **second terminal** and launch the Streamlit chat interface:

```bash
uv run streamlit run app.py

```

*This will automatically open the UI in your web browser at `http://localhost:8501`.*

---

## 📂 Project Structure

* `main.py` — The FastAPI backend router and startup lifecycle.
* `app.py` — The Streamlit chat interface and message state manager.
* `agent.py` — The LangGraph accountability coach agent, memory saver, and LLM configuration.
* `models.py` — SQLModel database schemas for habit tracking.
* `tools.py` — Custom LLM tools for creating, updating, and listing user habits.
* `habits.db` — SQLite database storing your active habits and track logs.
* `checkpoints.sqlite` — SQLite database preserving the LLM's chat history across restarts.