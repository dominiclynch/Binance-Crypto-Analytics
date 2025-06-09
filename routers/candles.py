"""Endpoints that proxy raw candle data from Data-Service."""
from fastapi import APIRouter, HTTPException, Query
import aiohttp

from settings import get_settings

router = APIRouter(prefix="/api", tags=["candles"])
settings = get_settings()


async def _fetch_json(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise HTTPException(status_code=resp.status, detail=text)
            return await resp.json(loads=None)


@router.get("/latest")
async def latest(symbol: str = Query("BTCUSDT", description="Symbol e.g. BTCUSDT")):
    """Return latest 1-minute candle for a symbol (proxy)."""
    api_url = f"{settings.data_api_url}/candles/{symbol}/1m?limit=1"
    data = await _fetch_json(api_url)
    return data[0] if isinstance(data, list) else data
