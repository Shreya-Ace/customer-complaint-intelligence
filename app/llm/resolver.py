from app.config import settings
from app.llm.client import GroqClient
from app.schemas.complaint import (
    ComplaintAnalysis,
    ResolutionSupport,
)


class ResolutionSupportGenerator:

    def __init__(self):
        self.llm = GroqClient()

        prompt_path = (
            settings.PROMPTS_DIR /
            "resolution_support.txt"
        )

        self.prompt_template = prompt_path.read_text(
            encoding="utf-8"
        )

    def generate(
        self,
        complaint: str,
        analysis: ComplaintAnalysis
    ) -> ResolutionSupport:

        prompt = self.prompt_template.format(
            complaint=complaint,
            analysis=analysis.model_dump_json(
                indent=2
            )
        )

        system_message = """
You are a customer-support resolution assistant.

Use only the information provided in the complaint
and analysis.

Do not invent:
- order numbers
- refund amounts
- delivery dates
- company policies
- actions that have already been performed

Return valid JSON only.
"""

        result = self.llm.generate_json(
            prompt=prompt,
            system_message=system_message
        )

        return ResolutionSupport(
            summary=result.get(
                "summary",
                ""
            ),
            recommended_actions=result.get(
                "recommended_actions",
                []
            ),
            suggested_response=result.get(
                "suggested_response",
                ""
            )
        )