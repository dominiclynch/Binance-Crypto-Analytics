# Binance Crypto Analytics

FastAPI analytics layer that merges ML model probabilities with live market data to produce actionable trading signals.

## What It Does

- Serves `/api/analysis` — combines latest candle prices with ML probability scores, emitting BUY_LONG/SHORT actions
- Serves `/api/signals` — returns filtered, execution-ready signal JSON from the ML engine
- Proxies candle data from the upstream Data Service and exposes Prometheus `/metrics`

## Tech Stack

- **Python:** FastAPI, aiohttp, Pydantic, prometheus_client

## Setup

```bash
pip install -r requirements.txt
export DATA_API_URL=http://localhost:8001
uvicorn app:app --host 0.0.0.0 --port 8080
```

## License

MIT
