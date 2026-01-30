from pydantic import BaseModel
from typing import List, Dict

class ImpactItem(BaseModel):
    event: str
    impact_level: str
    score: int
    why: List[str]
    actions: List[str]
    url: str

class ReportSchema(BaseModel):
    summary: str
    drivers: List[str]
    competitors: List[str]
    impact_radar: List[ImpactItem]
    opportunities: List[str]
    risks: List[str]
    ninety_day_plan: Dict[str, List[str]]
    sources: List[str]
