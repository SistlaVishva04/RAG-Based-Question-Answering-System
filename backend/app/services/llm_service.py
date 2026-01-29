import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing")

class LLMService:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.model = "gemini-2.5-flash"

    def generate_answer(self, context: str, query: str) -> str:
        prompt = f"""
You are a document question-answering system.

STRICT RULES:
- Use ONLY the information in the CONTEXT.
- Do NOT use any outside knowledge.
- If the answer is not explicitly present in the context, respond exactly with:
"I don't know based on the document."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text.strip()
