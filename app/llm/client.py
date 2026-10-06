import json
from typing import Any, Dict

from groq import Groq

from app.config import settings


class GroqClient:

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not configured. "
                "Add it to your .env file."
            )

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def generate(
        self,
        prompt: str,
        system_message: str = "You are a helpful NLP assistant."
    ) -> str:

        response = self.client.chat.completions.create(
            model=settings.GROQ_MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()

    def generate_json(
        self,
        prompt: str,
        system_message: str
    ) -> Dict[str, Any]:

        response = self.client.chat.completions.create(
            model=settings.GROQ_MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            response_format={
                "type": "json_object"
            },
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)

        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Groq returned invalid JSON:\n{content}"
            ) from exc