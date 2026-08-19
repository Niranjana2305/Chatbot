SAFE_FALLBACK = (
    "I'm sorry, but I cannot fulfill that response as it violates safe response guidelines. "
    "How else can I help with your habit goals today?"
)

FORBIDDEN_TERMS = [
    "HABIT_BUILDER_PROMPT",
    "checkpoints.sqlite",
    "long_term_store.sqlite",
    "SqliteSaver",
    "SqliteStore",
    "SYSTEM INSTRUCTIONS:",
    "SECURITY & INPUT HANDLING RULES:",
]

def apply_output_guardrail(response_content) -> str:
    """
    Evaluates final AI response text before returning it to the user.
    If system prompt names, DB connections, or prompt leaks are detected,
    returns a safe fallback message.
    """
    if isinstance(response_content, list):
        text = "".join([b.get("text", "") for b in response_content if isinstance(b, dict)])
    else:
        text = str(response_content)

    for term in FORBIDDEN_TERMS:
        if term.lower() in text.lower():
            return SAFE_FALLBACK

    return text