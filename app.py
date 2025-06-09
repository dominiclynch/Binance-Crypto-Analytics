"""Main FastAPI application entry-point."""
from datetime import datetime
from fastapi import FastAPI, Response
import prometheus_client

from routers import candles, analysis, signals

app = FastAPI(title="Crypto Analytics API", version="0.1.0")

# Include sub-routers
app.include_router(candles.router)
app.include_router(analysis.router)
app.include_router(signals.router)


@app.get("/healthz", tags=["meta"])
async def healthz():
    """Basic liveness probe."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    content = prometheus_client.generate_latest()
    return Response(content, media_type=prometheus_client.CONTENT_TYPE_LATEST)
