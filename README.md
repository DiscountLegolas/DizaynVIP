## Healthy Eating Chatbot – Getting Started

This project is a simple terminal-based healthy eating chatbot powered by OpenAI and LangChain.  
It lets you chat about healthy eating and see a quality **score** for each bot message.

### 1. Prerequisites
- **Python**: Make sure you have Python 3.9+ installed.
- **OpenAI API key**: You need a valid OpenAI API key.

### 2. Install dependencies
From the project folder (where `ChatBot.py` is located), run:

```bash
pip install -r requirements.txt
```

### 3. Get your OpenAI API key and create a `.env` file
- Go to the OpenAI website, create an account (if needed), and generate an **API key**.
- In the same folder as `ChatBot.py`, create a file named **`.env`**.
- Put your key in that file like this:

```text
OPENAI_TOKEN=your_openai_api_key_here
```

The app will automatically read this value when it starts.

### 4. Run the chatbot
From the project folder, run:

```bash
python ChatBot.py
```

You should see:
- A title `Healthy Eating Chatbot`
- A short introduction from the bot

### 5. How to talk to the bot and ask questions
- Type your message after the `You:` prompt and press **Enter**.
- Ask anything related to **healthy eating, nutrition, fruits & vegetables, hydration, balanced meals, processed foods, or meal timing**.
- The bot will respond as a friendly healthy eating enthusiast and you will see:
  - **Bot:** the chatbot’s reply
  - **Score:** a number from 0–100 showing the quality score of that reply
- To **exit**, type: `quit`, `exit`, or `q` and press **Enter**.

That’s all a new user needs to start the app and ask questions.


