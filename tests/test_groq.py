from groq import Groq
from app.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


response = client.chat.completions.create(
    model=settings.GROQ_MODEL,
    messages=[
        {
            "role": "user",
            "content": ""
        }
    ],
    temperature=0.2
)


print(response.choices[0].message.content)