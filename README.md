# 🏃 Habit Builder Coach & Secure Agent API

An intelligent, secure full-stack AI habit coaching application that helps users track daily habits, maintain streaks, receive verified exercise safety guidance using Retrieval-Augmented Generation (RAG), and enforce OWASP Top 10 for LLM security controls.

---

## 📌 Project Summary

The Habit Builder Bot combines interactive habit tracking with persistent long-term memory, grounded health advice, and production-grade LLM security controls. Built with LangChain, LangGraph, FastAPI, SQLModel, Streamlit, and Garak, it acts as a personal accountability coach while defending against prompt injections, persona hijacking, and secret leaks.

- **Habit Management & Tool Calling:** SQLite CRUD operations via structured tool calling for managing active goals, check-ins, and streak updates.
- **Cross-Session Long-Term Memory:** Powered by LangGraph's `SqliteStore`, persisting durable user profiles (motivations, preferences, past struggles) across session resets under a persistent `user_id`.
- **Grounded Health Guidance (RAG):** Automatically routes physical safety queries to a local FAISS vector database containing verified health guidelines with required medical disclaimers.
- **AI Application Security & Guardrails:** Implements untrusted input XML delimiters, untrusted knowledge base tag wrapping, OWASP LLM01 prompt engineering rules, an automated execution harness (`garak_harness.py`), and post-agent output guardrails.

---

## ✨ Key Features

- 🧠 **Cross-Session Long-Term Memory:** Retains persistent facts across thread resets and backend restarts using LangGraph `SqliteStore`.
- 👤 **Multi-User Identity Controls:** Streamlit sidebar allows switching between `user_id` profiles with active visual feedback badges.
- 📝 **Interactive Habit Tracking:** Create, list, update (frequency, description, or name), and delete custom habits.
- 🔥 **Automated Streak Maintenance:** Log check-ins and let the bot update and calculate streaks automatically in real time.
- 📚 **Grounded Health Guidance (RAG):** Local vector search (`FastEmbedEmbeddings()` + FAISS) providing grounded exercise safety answers with mandatory medical disclaimers.
- 🛡️ **OWASP LLM01 Prompt Injection Defenses:** System prompt operational boundaries, strict persona protection, and hard refusal protocols.
- 📦 **Input & Retrieval Delimiters:** Encapsulates incoming messages inside `<user_prompt>` and RAG context inside `<retrieved_data>` tags to separate instructions from data.
- 🔒 **Post-Agent Output Guardrails:** `output_guard.py` filters raw model responses before sending them back to the API client to prevent prompt leakage.
- ⚔️ **Automated Red-Teaming (Garak Integration):** Custom function harness (`garak_harness.py`) supporting Garak vulnerability scans across `promptinject`, `leakreplay`, and `dan` probes.
- 📊 **Verified Retrieval Quality:** Automated evaluation suite (`eval_rag.py`) verifying a 90%+ Hit Rate@k across safety queries.
- 🏷️ **Source Transparency:** UI display showing source badges (*Direct Answer* vs. *Verified Health KB*) with collapsible retrieved context passages.

---

## 🔒 AI Security & Guardrail Implementations

### 1. Input & RAG Context Delimiters
To defend against prompt injection and jailbreaks, all dynamic inputs are strictly isolated from system instructions using explicit structural tags:
- **User Input Tagging:** Encloses raw user messages inside `<user_prompt>...</user_prompt>` tags so the LLM explicitly recognizes incoming text as unverified data rather than actionable system commands ([OpenRouter Guardrails Guide](https://openrouter.ai/docs/guides/features/guardrails/prompt-injection)).
- **Retrieved Knowledge Tagging:** Encloses context fetched from the vector database inside `<retrieved_data>...</retrieved_data>` tags. System instructions explicitly dictate that contents within these tags are purely reference material and must never be executed as instructions or override system rules.

### 2. Prompt Engineering Defenses (OWASP LLM01)
Aligned with the [OWASP LLM01: Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) framework, the core system instructions instruct the model to enforce hard refusals:
- **Persona Protection:** Strictly refuses commands that attempt to alter its persona, adopt developer modes, or assume arbitrary roles.
- **System Confidentiality:** Denies requests attempting to extract system instructions, file architectures, database schemas, or secret tokens.
- **Function Call Verification:** Rejects attempts to run unverified tools or alter execution workflows.

### 3. Automated Red-Teaming with Garak
Using [Garak](https://docs.garak.ai/garak), an automated LLM vulnerability scanner, the system undergoes vulnerability testing by sending thousands of known attack prompts, encoded malicious inputs, and jailbreak payloads to verify system prompt confidentiality and test filter bypass resilience.

```powershell
# Run Garak Security Scan against agent harness
uv run garak --target_type function --target_name garak_harness#agent_target --generations 1 --spec probes.promptinject,probes.leakreplay,probes.dan

```

| Security Metric | Target Benchmark | Defense Mechanism |
| --- | --- | --- |
| **`probes.promptinject`** | $\ge$ 95% Pass Rate | XML Delimiters (`<user_prompt>`) + Strict Instruction Separation |
| **`probes.leakreplay`** | 100% Pass Rate | Prompt Confidentiality Rules + `output_guard.py` Filtering |
| **`probes.dan`** | $\ge$ 90% Pass Rate | Persona Protection & OWASP LLM01 Refusal Protocol |

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

### 4. Updating an Existing Habit
When you request changes to an active habit (e.g., changing its target frequency, updating description, or renaming it), the assistant executes update_habit to modify parameters cleanly without losing streak history.



<img width="354" height="301" alt="image" src="https://github.com/user-attachments/assets/000a4f35-675e-4ea1-bb08-8e52fb3366d2" />



---

### 5. Deleting a Habit
When you stop tracking a goal, asking to delete or remove it triggers the delete_habit tool, removing it from the database and returning confirmation feedback.



<img width="396" height="296" alt="Screenshot 2026-08-25 082303" src="https://github.com/user-attachments/assets/38159b7a-96f3-4973-9c2c-658cc0ed2b31" />



---

### 6. Verified Health Guidance (RAG Invocations)

*When asking health or safety questions, the assistant triggers `search_health_knowledge_base`, grounds its advice in retrieved passages, displays a safety disclaimer, and provides an expandable view of source context.*


<img width="543" height="300" alt="Screenshot 2026-07-28 071542" src="https://github.com/user-attachments/assets/b87b88c7-f79c-4b60-ad6e-944f81818982" />


---

### 7. Cross-Session Long-Term Memory Recall

When starting a brand-new conversation thread, the assistant invokes get_user_profile, reads persistent facts stored in LangGraph's SqliteStore under your User ID, and accurately recalls your motivations and preferences without needing prior chat context.



<img width="449" height="196" alt="Screenshot 2026-08-04 074650" src="https://github.com/user-attachments/assets/cf5f1d8e-b5b7-4be5-b926-66a60f106c14" />





<img width="455" height="150" alt="Screenshot 2026-08-04 074656" src="https://github.com/user-attachments/assets/a8a2b675-57d2-40b8-9617-16e3e57a9ece" />

---

### 8. Automated Security Refusal

*Direct prompt injection attempts trigger the standardized security refusal message without exposing internal system instructions or state.*



<img width="539" height="142" alt="image" src="https://github.com/user-attachments/assets/85e0198d-6130-4b0f-942f-7b11f66437f1" />



---

## 🏗️ Tech Stack

| Component | Technology Used |
| --- | --- |
| **Frontend UI** | Streamlit |
| **Backend API** | FastAPI + Uvicorn |
| **Agent Framework** | LangChain / LangGraph |
| **Long-Term Memory** | LangGraph `SqliteStore` (Cross-Session) |
| **Short-Term Memory** | LangGraph `SqliteSaver` (Thread Checkpointer) |
| **Embeddings Model** | HuggingFace (`FastEmbedEmbeddings()`) |
| **Vector Store** | FAISS |
| **Database & ORM** | SQLite + SQLModel |
| **LLM Vulnerability Scanner** | Garak (`garak_harness.py`) |
| **Package Manager** | `uv` |

---

## 🚀 Quick Start Guide

### Prerequisites

* Python 3.14+
* [`uv`](https://docs.astral.sh/uv/) installed on your machine

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
# MODEL_NAME=google_genai:gemini-1.5-flash
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

### 5. Execute Garak Security Vulnerability Scan

```bash
uv run garak --target_type function --target_name garak_harness#agent_target --generations 1 --spec probes.promptinject,probes.leakreplay,probes.dan

```

### 6. Run the Backend API

Start the FastAPI server:

```bash
uv run uvicorn main:app --reload --port 8000

```

*Backend runs at:* `http://127.0.0.1:8000`

### 7. Launch the Streamlit Frontend

In a new terminal window:

```bash
uv run streamlit run app.py

```

*Frontend launches at:* `http://localhost:8501`

---

## 📂 Project Structure

```text
├── knowledge_base/         # Markdown files with exercise safety & health guidelines
│   ├── 01_emergency_red_flags.txt
│   ├── 02_exercise_safety_progression.txt
│   ├── 03_overtraining_recovery.txt
│   └── ...
├── build_kb.py             # Generates FAISS vector index from knowledge base files
├── eval_rag.py             # Evaluates vector retrieval accuracy (Hit Rate@k)
├── rag.py                  # FAISS similarity search tool implementation
├── tools.py                # CRUD tools for habit tracking and memory management
├── models.py               # SQLModel schemas for local SQLite storage
├── output_guard.py         # Post-agent filtering logic for output guardrails
├── garak_harness.py        # Custom harness module for Garak red-teaming scans
├── agent.py                # LangGraph agent orchestration, memory, & prompt definition
├── main.py                 # FastAPI backend handling chat endpoints & guardrails
└── app.py                  # Streamlit chat interface with identity controls

```

```

```
