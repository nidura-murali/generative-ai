from groq import Groq
import logging
from schemas import AppError
class GroqLLMClient:
    def __init__(self):
        self.client = Groq(api_key="your key")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
         logging.error("Unexpected LLM failure: %s", str(e))
         errorMessage = "Unexpected LLM failure:"+ str(e)
         raise AppError("500",errorMessage)