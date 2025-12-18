from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy
from langchain_openai import ChatOpenAI
from Tool import score_message_tool
from langgraph.checkpoint.memory import InMemorySaver    
import os
from dotenv import load_dotenv
load_dotenv()
class ChatResponse(BaseModel):
    """
    Structured response returned by the agent.
    """
    message: str  
    score: float 




system_prompt = """You are a friendly and knowledgeable nutrition enthusiast 
who loves discussing healthy eating habits. You're having a casual conversation with someone 
about their thoughts on healthy eating and nutrition. 

Your role:
- Be conversational, warm, and engaging
- Ask open-ended questions to encourage discussion
- Show genuine interest in the person's perspective
- Guide the conversation naturally toward topics like fruits & vegetables, hydration, 
  balanced meals, processed foods, and meal timing
- Don't lecture or be preachy - keep it friendly and conversational
- Respond naturally as if you're chatting with a friend about nutrition

When you answer:
- First, think step-by-step about the best, friendliest reply to the **user's input**.
- Then, use the `score_message` tool on the **user's latest message** to get a score for their input.
- Finally, fill the `ChatResponse` fields so that:
  - `message` is your final reply text.
  - `score` is the numeric score (0–100) you inferred from the tool result for the **user's input**.

Start the conversation by introducing yourself and asking about their thoughts on healthy eating."""
API_KEY=os.getenv("OPENAI_TOKEN")
chat_model = ChatOpenAI(model="gpt-4o-mini",max_completion_tokens=512,api_key=API_KEY)

agent = create_agent(
    chat_model,
    system_prompt=system_prompt,
    tools=[score_message_tool],
    response_format=ProviderStrategy(ChatResponse),
    checkpointer=InMemorySaver())


def run_chat() -> None:
    thread_id = "1"

    print("Nutrition Chatbot")
    print("Type 'quit' or 'exit' to end the conversation.\n")

    print("Bot: Hi! I'm your friendly nutrition chat companion.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Bot: It was great chatting about nutrition with you. Take care!")
            break

        if not user_input:
            continue

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            },
            {"configurable": {"thread_id": thread_id}},
        )

        sr = result["structured_response"]
        print("Bot:", sr.message)
        print("Score:", sr.score)


if __name__ == "__main__":
    run_chat()