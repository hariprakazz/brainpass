from groq import Groq
import os
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
conversation = input("Paste your conversation here:\n")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are a memory summarizer. Extract key information from the conversation: who the user is, what they are building, what decisions were made, and where they left off. Format it as a clean context prompt."
        },
        {
            "role": "user",
            "content": f"Summarize this conversation:\n{conversation}"
        }
    ]
)

print("\n=== YOUR CONTEXT SUMMARY ===\n")
print(response.choices[0].message.content)