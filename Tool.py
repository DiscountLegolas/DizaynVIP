from typing import Any, Dict

from Helper import detect_keywords, evaluate_response
from langchain.tools import tool


def score_message(response: str) -> Dict[str, Any]:
    """
    Simple helper function (NOT a LangChain tool) that scores a message
    based on the keywords and context and returns structured data.

    Args:
        response: The text to be evaluated.

    Returns:
        A dictionary containing the numeric score, per-category breakdown,
        and raw keyword detection results.
    """
    keyword_results = detect_keywords(response)
    score, breakdown = evaluate_response(response, keyword_results)

    return {
        "score": score
    }


@tool("score_message")
def score_message_tool(response: str) -> Dict[str, Any]:
    """
    LangChain tool wrapper around the `score_message` helper.

    This tool returns structured output so the agent can easily read
    the numeric score and detailed breakdown.
    """
    return score_message(response)
