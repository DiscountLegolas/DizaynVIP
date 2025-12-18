from typing import Any, Dict

from Helper import detect_keywords, evaluate_response
from langchain.tools import tool


def score_message(user_text: str) -> Dict[str, Any]:
    """
    Simple helper function (NOT a LangChain tool) that scores the **user's input**
    based on the keywords and context and returns structured data.

    Args:
        user_text: The user's input text to be evaluated.

    Returns:
        A dictionary containing the numeric score (0–100).
    """
    keyword_results = detect_keywords(user_text)
    score, breakdown = evaluate_response(user_text, keyword_results)

    return {
        "score": score
    }


@tool("score_message")
def score_message_tool(user_text: str) -> Dict[str, Any]:
    """
    LangChain tool wrapper around the `score_message` helper.

    This tool scores the **user's input message**, not the assistant's response.
    It returns structured output so the agent can easily read the numeric score.
    """
    return score_message(user_text)
