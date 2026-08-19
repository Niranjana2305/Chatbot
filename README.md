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
- 📝 **Interactive Habit Tracking:** Create custom habits with specific target frequencies (daily, weekly, custom interval).
- 🔥 **Automated Streak Maintenance:** Log check-ins and let the bot update and calculate streaks automatically in real time.
- 📚 **Grounded Health Guidance (RAG):** Local vector search (`sentence-transformers/all-MiniLM-L6-v2` + FAISS) providing grounded exercise safety answers with mandatory medical disclaimers.
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
