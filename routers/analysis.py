"""/api/analysis – combine latest candle + probability."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import List

import aiohttp
from fastapi import APIRouter, HTTPException

from schemas import AnalysisEntry, AnalysisResponse
from settings import get_settings

router = APIRouter(prefix="/api", tags=["analysis"])
settings = get_settings()


async def _fetch_latest_candle(symbol: str):
    url = f"{settings.data_api_url}/candles/{symbol}/1m?limit=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail=f"Upstream error for {symbol}")
            data = await resp.json(loads=None)
            return data[0] if isinstance(data, list) else data


@router.get("/analysis", response_model=AnalysisResponse)
async def analysis() -> AnalysisResponse:
    probs_file = Path(settings.signals_dir) / "latest_probs.json"
    if not probs_file.exists():
        raise HTTPException(status_code=404, detail="latest_probs.json not found yet")

    probabilities = json.loads(probs_file.read_text())
    opps: List[AnalysisEntry] = []
    for symbol, proba in probabilities.items():
        candle = await _fetch_latest_candle(symbol)
        simple_action: str | None = None
        if proba >= 0.6:
            simple_action = "BUY_LONG"
        elif proba <= 0.4:
            simple_action = "SHORT"
        opps.append(
            AnalysisEntry(
                symbol=symbol,
                probability=round(proba, 4),
                simple_action=simple_action,
                current_price=float(candle[4] if isinstance(candle, list) else candle.get("close", 0.0)),
                timestamp=datetime.utcnow().isoformat() + "Z",
            )
        )

    return AnalysisResponse(timestamp=datetime.utcnow().isoformat() + "Z", opportunities=opps)
