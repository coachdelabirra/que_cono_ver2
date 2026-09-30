# Base44 Dev Environment

## Stack
- **Python + Streamlit** single-file app (`app.py`), SQLite local DB (`db.py`).
- No external services, no secrets, no APIs required. Fully self-contained.

## Running
- `docker compose -f docker-compose.base44.yml up -d` brings up the app on host port 3000 (container port 8501).
- Base image: `python:3.12-slim`. Dependencies (`streamlit`, `pillow`) install on container startup from `requirements.txt`.
- Source is bind-mounted at `/app`; edits hot-reload via Streamlit's file watcher.

## Key details
- Streamlit runs with `--server.enableCORS=false` (counterintuitively, `enableCORS=True` *restricts* websocket origins to localhost/IPs only; `False` allows all origins), `--server.enableXsrfProtection=false`, and `--server.allowedHosts=*` so the preview proxy can reach it.
- SQLite DB file lives at `data/quecono.db` (gitignored, created on first run). Poster uploads go to `data/posters/`.
- Health endpoint: `/_stcore/health` (returns 200 when Streamlit is ready).
- Login is username + 4-digit PIN (hashed with salt in SQLite). No external auth.

## Verifying
- `curl http://localhost:3000/_stcore/health` → HTTP 200.
- Preview shows the NES-styled "Que coño ver?" login screen.
