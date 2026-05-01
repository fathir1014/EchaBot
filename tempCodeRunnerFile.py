from groq import Groq

client = Groq(api_key="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")

messages = [
    {
        "role": "system",
        "content": "You are a strict Python generator. ONLY output valid Python code. No explanation."
    }
]

print("===  Echabot (type 'exit' to quit) ===")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=messages
    )

    reply = response.choices[0].message.content

    print("\nBot:\n", reply, "\n")

    messages.append({
        "role": "assistant",
        "content": reply
    })