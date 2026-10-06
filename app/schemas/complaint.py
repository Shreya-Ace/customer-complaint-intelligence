from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ComplaintEntities(BaseModel):
    product: Optional[str] = None
    order_id: Optional[str] = None
    date: Optional[str] = None
    amount: Optional[str] = None
    location: Optional[str] = None
    organization: Optional[str] = None
    duration: Optional[str] = None


class ComplaintAnalysis(BaseModel):
    category: str
    intent: str
    sentiment: str
    urgency: str
    entities: ComplaintEntities


class ResolutionSupport(BaseModel):
    summary: str
    recommended_actions: List[str]
    suggested_response: str


class ComplaintResult(BaseModel):
    complaint: str
    analysis: ComplaintAnalysis
    resolution: ResolutionSupport


class ComplaintRequest(BaseModel):
    complaint: str = Field(
        ...,
        min_length=5,
        description="Customer complaint text"
    )