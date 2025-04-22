import os
from dotenv import load_dotenv, find_dotenv
from google import genai

load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def gemini(query: str = "Tell me about the latest world affairs."):
    client = genai.Client(api_key=GEMINI_API_KEY)

    with open('llm/system_prompt.txt', 'r') as file:
        sys_directive = file.read().strip()

    query = query + str(sys_directive) # rag lol

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite", 
        contents=query
    )

    return response.text
