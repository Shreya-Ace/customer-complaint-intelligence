from app.config import settings
from app.llm.client import GroqClient
from app.nlp.entities import extract_entities
from app.nlp.sentiment import analyze_sentiment
from app.schemas.complaint import (
    ComplaintAnalysis,
    ComplaintEntities,
)


class ComplaintAnalyzer:

    def __init__(self):
        self.llm = GroqClient()

        prompt_path = (
            settings.PROMPTS_DIR /
            "complaint_analysis.txt"
        )

        self.prompt_template = prompt_path.read_text(
            encoding="utf-8"
        )

    def analyze(self, complaint: str) -> ComplaintAnalysis:

        # Traditional NLP sentiment analysis
        sentiment = analyze_sentiment(complaint)

        # Traditional NLP entity extraction
        entities = extract_entities(complaint)

        # Insert the NLP results into the LLM prompt
        prompt = self.prompt_template.format(
            complaint=complaint,
            sentiment=sentiment,
            entities=entities
        )

        system_message = """
You are an NLP system for customer complaint analysis.

Your task is to classify complaints accurately and
return only valid JSON.

Never invent information that is not present in the
complaint.
"""

        # Send the complaint + NLP results to Groq
        result = self.llm.generate_json(
            prompt=prompt,
            system_message=system_message
        )

        return ComplaintAnalysis(
            category=result.get(
                "category",
                "Other"
            ),
            intent=result.get(
                "intent",
                "Unknown"
            ),
            sentiment=result.get(
                "sentiment",
                sentiment
            ),
            urgency=result.get(
                "urgency",
                "Medium"
            ),
            entities=ComplaintEntities(
                **result.get(
                    "entities",
                    {}
                )
            )
        )