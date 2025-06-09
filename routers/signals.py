"""/api/signals – serve actionable filtered signals JSON."""
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from settings import get_settings

router = APIRouter(prefix="/api", tags=["signals"])
settings = get_settings()


@router.get("/signals")
async def signals() -> Any:
    file_path = Path(settings.signals_dir) / "latest_signals.json"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="latest_signals.json not found yet")
    data = json.loads(file_path.read_text())
    return {"timestamp": datetime.utcnow().isoformat() + "Z", "signals": data}
