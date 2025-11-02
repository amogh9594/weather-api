# Weather API (FastAPI) — Simple, no-key weather API

A tiny FastAPI application that fetches live weather (via `wttr.in`) and exposes:
- `/weather?city=CityName` — current weather
- `/forecast?city=CityName` — 3-day forecast

This repository contains everything needed to run locally or deploy to a host (Render, Vercel, Deta, etc.).

---

## Files
- `main.py` — main FastAPI app (defines `app = FastAPI()`).
- `requirements.txt` — Python dependencies.
- `vercel.json` — config for Vercel deployments.
- `README.md` — this file.

---

## Quick start (local)
1. Create & activate a virtualenv (optional but recommended):
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   
2. Install dependencies:
   `pip install -r requirements.txt`

3. Run with Uvicorn:
    `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`

4. Test:
   4.1. `http://127.0.0.1:8000/`
   4.2. `http://127.0.0.1:8000/weather?city=London`
   4.3. `http://127.0.0.1:8000/forecast?city=London`

