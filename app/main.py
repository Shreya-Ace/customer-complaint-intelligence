from fastapi import FastAPI, HTTPException

from app.config import settings
from app.llm.analyzer import ComplaintAnalyzer
from app.llm.resolver import ResolutionSupportGenerator
from app.schemas.complaint import (
    ComplaintRequest,
    ComplaintResult,
)


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "NLP and LLM-based customer complaint "
        "analysis and resolution support system."
    ),
    version="1.0.0",
)


# Initialize components once when the application starts.
analyzer = ComplaintAnalyzer()
resolver = ResolutionSupportGenerator()


@app.get("/")
def root():
    return {
        "message": "Customer Complaint Intelligence API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
    }


@app.post(
    "/analyze",
    response_model=ComplaintResult,
)
def analyze_complaint(
    request: ComplaintRequest,
):

    try:
        # Component 1 + 2
        analysis = analyzer.analyze(
            request.complaint
        )

        # Component 3
        resolution = resolver.generate(
            complaint=request.complaint,
            analysis=analysis,
        )

        return ComplaintResult(
            complaint=request.complaint,
            analysis=analysis,
            resolution=resolution,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )