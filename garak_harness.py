# garak_harness.py
from typing import List, Union
from agent import get_safe_response

def agent_target(prompt: str, **kwargs) -> List[str]:
    """
    Harness wrapper for Garak red-teaming.
    Explicitly returns List[str] with 1 item to satisfy Garak's generator requirements.
    """
    try:
        response = get_safe_response(
            user_input=prompt,
            user_id="garak_redteam_user",
            thread_id="garak_security_session"
        )
        
        # 1. Handle generator/stream objects if get_safe_response streams tokens
        if hasattr(response, "__iter__") and not isinstance(response, (str, dict)):
            # If it's a generator or token stream, join chunks together
            cleaned_text = "".join(
                chunk.content if hasattr(chunk, "content") else str(chunk) 
                for chunk in response
            )
        # 2. Handle LangChain AIMessage / BaseMessage objects
        elif hasattr(response, "content"):
            cleaned_text = str(response.content)
        # 3. Handle dictionary returns (e.g., {"output": "..."})
        elif isinstance(response, dict) and "output" in response:
            cleaned_text = str(response["output"])
        # 4. Standard string or fallback
        else:
            cleaned_text = str(response)

        # Garak expects a list of string generations
        return [cleaned_text]

    except Exception as e:
        return [f"Error processing prompt: {str(e)}"]