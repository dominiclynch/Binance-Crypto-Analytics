"""Pydantic response models."""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Candle(BaseModel):
    symbol: str
    timestamp: int | str
    open: float
    high: float
    low: float
    close: float
    volume: float


class AnalysisEntry(BaseModel):
    symbol: str
    probability: float = Field(..., ge=0.0, le=1.0)
    simple_action: Optional[str]
    current_price: float
    timestamp: str


class AnalysisResponse(BaseModel):
    timestamp: str
    opportunities: List[AnalysisEntry]
