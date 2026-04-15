
#CORE LLM CLIENT — core/llm_client.py


#from core.rag import retrieve_relevant_chunks

import os
from dotenv import load_dotenv
from groq import Groq

# 🔥 Load .env file
load_dotenv()


# 🔐 Load API Key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not set in environment variables")

# Initialize client
client = Groq(api_key=GROQ_API_KEY)


def ask_llm(prompt: str) -> str:
    print("\n🚀 GROQ CALL INITIATED")
    print("🔑 API KEY PRESENT:", bool(os.getenv("GROQ_API_KEY")))
    print("🧾 PROMPT LENGTH:", len(prompt))

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024,
        )

        response = completion.choices[0].message.content

        print("✅ GROQ RESPONSE RECEIVED")
        print("📏 RESPONSE LENGTH:", len(response))

        return response.strip()

    except Exception as e:
        print("❌ GROQ ERROR:", str(e))
        return f"LLM Error: {str(e)}"


"""
def ask_llm(prompt: str) -> str:
    print("\n🚀 Sending request to Groq...")

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        response = completion.choices[0].message.content

        print("\n✅ FINAL RESPONSE:", response)

        return response.strip()

    except Exception as e:
        print("❌ LLM ERROR:", str(e))
        return "Error: LLM request failed."

"""

"""
client = ollama.Client(host='http://127.0.0.1:11434')
MAX_CHARS = 3000  # safe starting point

def ask_llm(prompt):

    if len(prompt) > MAX_CHARS:
        prompt = prompt[:MAX_CHARS]
        print("⚠ Prompt truncated for performance.")

    print("\n>>> Sending prompt to Ollama\n")

    stream = client.chat(
        model="llama3.2:latest",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    full_response = ""

    for chunk in stream:
        content = chunk["message"]["content"]
        print(content, end="", flush=True)
        full_response += content

    print(f"\n")
    return full_response
"""


"""
MAX_CHARS = 3000  # safe starting point

def ask_llm(prompt):

    if len(prompt) > MAX_CHARS:
        prompt = prompt[:MAX_CHARS]
        print("⚠ Prompt truncated for performance.")

    print(">>> Sending prompt to Ollama")

    response = ollama.chat(
        #model="llama3",
        model="llama3.2:latest",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    return response["message"]["content"]
"""


