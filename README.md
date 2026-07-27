Here is the updated, clean `README.md` reflecting your current architecture—including the **Knowledge Base (RAG)** pipeline, the fix for model naming without prefixes, and vector store generation instructions.

---

```markdown
# Habit Builder Bot 🚀

Welcome to the **Habit Builder Bot**—your personal, AI-powered habit and accountability coach. This application features a robust **FastAPI** backend running a LangChain/LangGraph agent with RAG knowledge base retrieval, paired with an interactive **Streamlit** frontend UI.

---

## 🛠️ Prerequisites

Before getting started, make sure you have **`uv`** installed on your system for fast dependency management and virtual environment handling.

If you haven't installed `uv`, install it via PowerShell/Terminal:
```powershell
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

```

---

## ⚙️ Setup Instructions

Follow these steps to set up and run the application locally:

### 1. Clone the Repository

```bash
git clone [https://github.com/Niranjana2305/Chatbot.git](https://github.com/Niranjana2305/Chatbot.git)
cd Chatbot

```

### 2. Install Dependencies

Use `uv` to automatically create a virtual environment and sync all required packages:

```bash
uv sync

```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env

```

Open `.env` and fill in your model configuration and API keys:

```env
# Model Name (e.g., llama-3.3-70b-versatile)
MODEL_NAME=llama-3.3-70b-versatile

# Add your API keys
GROQ_API_KEY=your_groq_api_key_here

```

### 4. Build the Health Knowledge Base (RAG Vectorstore)

Before starting the chatbot, generate the FAISS vector database from your markdown/text documents:

```bash
uv run python build_kb.py

```

*(This generates the local `faiss_index/` directory used by the coach to answer health and safety queries.)*

---

## 🚀 Running the Application

To run the application, start the backend server first, followed by the frontend interface.

### Step 1: Start the FastAPI Backend (First)

The backend initializes the SQLite database tables on startup and runs the AI agent. Run this in your first terminal:

```bash
uv run uvicorn main:app --reload

```

The backend will be live at `http://127.0.0.1:8000`.

### Step 2: Start the Streamlit Frontend (Second)

Open a second terminal and launch the Streamlit chat interface:

```bash
uv run streamlit run app.py

```

This will automatically open the UI in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

* **`main.py`** — The FastAPI backend router, message filtering logic, and startup lifecycle.
* **`app.py`** — The Streamlit chat interface, RAG expander display, and message state manager.
* **`agent.py`** — The LangChain accountability coach agent, system prompt, and LLM configuration.
* **`tools.py`** — Custom LLM tools for habit management (`add_habit`, `list_habits`, `log_checkin`) and health knowledge base searches (`search_health_knowledge_base`).
* **`models.py`** — SQLModel database schemas and streak calculation utilities.
* **`build_kb.py`** — Embeddings generator script that builds the local FAISS vector store.
* **`knowledge_base/`** — Plaintext & markdown document store for health, safety, and exercise recovery guidelines.
* **`habits.db`** — SQLite database storing active user habits and streak logs.

```

```
