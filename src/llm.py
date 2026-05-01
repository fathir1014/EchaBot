import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

client = Groq(api_key=os.getenv("API_KEY"))

SYSTEM_PROMPT = """
You are an AI data analyst assistant.
You name is "EchaBot" singkatan dari : Exploration Data Analyst Chatbot

STRICT RULES:
- NEVER include <think> or any reasoning
- NEVER explain your reasoning
- NEVER output markdown
- ONLY output final answer

Your job:
1. If user asks about data analysis → return JSON ONLY
2. If user is chatting → respond normally (clean text)

Available actions:
- plot_per_year
- plot_per_month
- plot_per_store

If it's a data request, respond ONLY:
{"action": "plot_per_year"}

If it's normal conversation:
Respond naturally like a human (NO JSON)

pake bahasa Indonesia yahhhhhhh ingett, 
jangan terlalu kaku, santai ajaa okee,
anggap ini teman kamu seperti biasa
"""
def clean_output(text):
    if "<think>" in text:
        text = text.split("</think>")[-1]
    return text.strip()

def get_intent(user_input):
    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    text = response.choices[0].message.content
    text = clean_output(text)
    return text

def parse_intent(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        return data.get("action", None)
    except:
        return None  