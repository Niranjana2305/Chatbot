
# 🏃 Habit Builder Coach

An intelligent, full-stack AI habit coaching application that helps users track daily habits, maintain streaks, and receive verified exercise safety guidance using Retrieval-Augmented Generation (RAG).

---

## 📌 Project Summary

The Habit Builder Bot combines interactive habit tracking with persistent long-term memory and safety-focused conversational AI. Built with LangChain (v1), LangGraph, FastAPI, SQLModel, and Streamlit, it acts as a personal accountability coach while ensuring users stay safe during physical activities.

Habit Management & Tool Calling: For standard habit operations (adding habits, listing active goals, logging check-ins, or tracking streaks), the AI interacts directly with a SQLite database via structured tool calls.

Cross-Session Long-Term Memory: Powered by LangGraph's SqliteStore, the agent persists durable user profile facts (motivations, preferred coaching style, family context, past struggles) across different chat sessions and thread IDs under a persistent user_id.

Grounded Health Guidance (RAG): When users express concerns about physical symptoms, overtraining, chest pain, or exercise safety, the system automatically routes queries to a local FAISS vector database containing verified health guidelines to provide grounded, safety-first answers with mandatory medical disclaimers.

---

## ✨ Key Features

  - 🧠 Cross-Session Long-Term Memory: Remembers user motivations, goals, and preferred coaching styles across thread resets and backend restarts using LangGraph's SqliteStore.
  - 👤 Multi-User Identity Controls: Streamlit sidebar input allows seamless switching between user_id profiles with instant visual feedback badges (✅ Active User ID).
  - 📝 Interactive Habit Tracking: Create custom habits with specific target frequencies (daily, weekly, custom interval).
  - 🔥 Automated Streak Maintenance: Log check-ins and let the bot update and calculate streaks automatically in real time.
  - 📚 Grounded Health Guidance (RAG): Uses local vector search (sentence-transformers/all-MiniLM-L6-v2 + FAISS) to answer exercise safety and injury questions using verified knowledge base files.
  - 📊 Verified Retrieval Quality: Built-in automated evaluation suite (eval_rag.py) verifying a 90%+ Hit Rate@k across safety and training queries.
  - 🏷️ Source Transparency: The UI displays an explicit source badge (Direct Answer vs. Verified Health KB) and offers a collapsible view of the exact retrieved context passages.
  - 🛡️ Safety & Disclaimers: Automatic detection of critical health symptoms (e.g., chest pain, severe soreness) with required medical disclaimers.
  - 💾 Persistent Chat State: Thread-level short-term state checkpointing via SqliteSaver combined with long-term memory via SqliteStore.

---

## 📸 Screenshots & Visual Walkthrough

### 1. Adding a New Habit Goal
*When you ask the assistant to start tracking a new goal, it invokes the `add_habit` tool to register the habit and initialize its streak counter in the database.*

<img width="475" alt="Screenshot 2026-07-28 071336" src="https://github.com/user-attachments/assets/0f1367ed-9d2b-4430-b96b-ae7f0d54949b" />

---

### 2. Logging a Check-in & Updating Streaks
*When you log progress for a habit, the assistant runs `log_checkin`, verifies the last check-in date, increments your streak counter, and provides encouraging feedback.*

<img width="447" height="136" alt="Screenshot 2026-07-28 073205" src="https://github.com/user-attachments/assets/59a5b224-0034-486f-96a6-f7b3c6ed081a" />

---

### 3. Listing Active Habits & Formatted Streaks
*Asking to view active habits calls `list_habits` and returns a clean, structured text list with streak numbers and last check-in timestamps.*


<img width="514" height="200" alt="Screenshot 2026-07-28 071845" src="https://github.com/user-attachments/assets/f48c49ed-f0f1-479a-8fa8-3914f7fcfbda" />

---

### 4. Verified Health Guidance (RAG Invocations)
*When asking health or safety questions, the assistant triggers `search_health_knowledge_base`, grounds its advice in retrieved passages, displays a safety disclaimer, and provides an expandable view of source context.*

<img width="543" height="300" alt="Screenshot 2026-07-28 071542" src="https://github.com/user-attachments/assets/b87b88c7-f79c-4b60-ad6e-944f81818982" />

---

### 5. Cross-Session Long-Term Memory Recall
When starting a brand-new conversation thread, the assistant invokes get_user_profile, reads persistent facts stored in LangGraph's SqliteStore under your User ID, and accurately recalls your motivations and preferences without needing prior chat context.

<img width="449" height="196" alt="Screenshot 2026-08-04 074650" src="https://github.com/user-attachments/assets/cf5f1d8e-b5b7-4be5-b926-66a60f106c14" />


<img width="455" height="150" alt="Screenshot 2026-08-04 074656" src="https://github.com/user-attachments/assets/a8a2b675-57d2-40b8-9617-16e3e57a9ece" />

---
## 🏗️ Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend UI** | Streamlit |
| **Backend API** | FastAPI + Uvicorn |
| **Agent Framework** | LangChain / LangGraph |
| **Long-Term Memory** | LangGraph SqliteStore (Cross-Session / Cross-Thread) |
| **Short-Term Memory** | LangGraph SqliteSaver (Per-Thread Checkpointer) |
| **Embeddings Model** | HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`) |
| **Vector Store** | FAISS |
| **Database** | SQLite + SQLModel (ORMs) |
| **Package Manager** | `uv` |

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) installed on your machine

### 1. Clone the Repository & Setup Environment
```bash
git clone [https://github.com/your-username/habit-builder-bot.git](https://github.com/your-username/habit-builder-bot.git)
cd habit-builder-bot

# Install dependencies using uv
uv sync

```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
MODEL_NAME=groq:llama-3.3-70b-versatile
# OR for Google Gemini:
# MODEL_NAME=gemini:gemini-1.5-flash
# GOOGLE_API_KEY=your_google_api_key_here

```

### 3. Build the Vector Knowledge Base

Build the local FAISS vector index from the Markdown files in `knowledge_base/`:

```bash
uv run python build_kb.py

```
### 4. (Optional) Run RAG Evaluation Benchmark

Validate vector retrieval quality against sample health queries:

```bash
uv run python eval_rag.py

```

### 5. Run the Backend API

Start the FastAPI server:

```bash
uv run uvicorn main:app --reload

```

*Backend runs at:* `http://127.0.0.1:8000`

### 6. Launch the Streamlit Frontend

In a new terminal window:

```bash
uv run streamlit run app.py

```

*Frontend launches at:* `http://localhost:8501`

---

## 📂 Project Structure

```text
├── knowledge_base/         # Markdown files with exercise safety & health guidelines
│   ├── 01_emergency_red_flags.md
│   ├── 02_exercise_safety_progression.md
│   ├── 03_overtraining_recovery.md
│   ├── 04_sleep_hydration_nutrition.md
│   ├── 05_mental_health_burnout.md
│   ├── 06_warmup_cooldown_stretching.txt
│   ├── 07_joint_pain_vs_muscle_soreness.txt
│   ├── 08_cardio_and_strength_pacing.txt
│   ├── 09_environmental_safety_heat_cold.txt
│   └── 10_nutrition_and_fueling_timing.txt
├── build_kb.py             # Script to chunk text and generate FAISS vector index
├── eval_rag.py              # Benchmark script measuring RAG Hit Rate@k retrieval accuracy
├── rag.py                  # LangChain tool wrapper for local FAISS similarity search
├── tools.py                # CRUD tools for habits, streaks, and long-term memory store
├── models.py               # SQLModel database schemas (HabitTrackerModel)
├── agent.py                # Core LangChain agent, SqliteStore & SqliteSaver setup
├── main.py                 # FastAPI backend handling /chat endpoints & payload parsing
└── app.py                  # Streamlit UI with user_id management & chat state

```
