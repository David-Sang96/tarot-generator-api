# Tarot Card Generation API

A small FastAPI app. It draws one random tarot card from a full 78-card deck,
upright or reversed, and returns the card's general meaning as JSON.
There is no database. The card data is in `app/data/tarot.yaml`.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Run (development server)

```bash
uv run fastapi dev app/main.py --host 0.0.0.0
```

`--host 0.0.0.0` makes the server listen on all network interfaces, so other
computers can call it, not only this one. The server runs on port 8000.

- On this computer: http://127.0.0.1:8000 (API docs at http://127.0.0.1:8000/docs)
- From another computer: `http://<this computer's IP>:8000`

This is the development server, with auto-reload and public API docs. Do not
leave it open to the internet for a long time.

To allow only this computer, remove `--host 0.0.0.0`.

## Run (production)

Production uses [Gunicorn](https://gunicorn.org/) with Uvicorn workers.
Gunicorn starts several worker processes and restarts a worker if it crashes.
There is no auto-reload.

```bash
uv sync --no-dev
uv run --no-dev gunicorn app.main:app
```

The settings are in `gunicorn.conf.py`, and Gunicorn reads this file
automatically. By default, the server listens on `0.0.0.0:8000` with one
worker per CPU core (at most 4).

| Environment variable  | Default        | Meaning                              |
|-----------------------|----------------|--------------------------------------|
| `GUNICORN_BIND`       | `0.0.0.0:8000` | Address and port to listen on        |
| `GUNICORN_WORKERS`    | CPU cores, max 4 | Number of worker processes         |
| `GUNICORN_TIMEOUT`    | `30`           | Seconds before a stuck worker restarts |
| `GUNICORN_LOG_LEVEL`  | `info`         | Log level                            |

### Run as a service (systemd)

`deploy/tarot-api.service` starts the API when the server boots and restarts
it if it stops. It expects the project in `/opt/tarot-generator-api` and the
user `ubuntu-server`.

```bash
sudo cp deploy/tarot-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now tarot-api
```

Useful commands:

```bash
sudo systemctl status tarot-api     # Is it running?
sudo journalctl -u tarot-api -f     # Follow the logs
sudo systemctl reload tarot-api     # Restart workers after a code update
sudo systemctl restart tarot-api    # Full restart
```

## Endpoint

`GET /v1/api/tarot-generate`

```bash
curl http://127.0.0.1:8000/v1/api/tarot-generate
```

```json
{
  "name": "The Star",
  "arcana": "major",
  "suit": null,
  "orientation": "upright",
  "meaning": "Hope, faith, rejuvenation."
}
```

| Field         | Values                                              |
|---------------|-----------------------------------------------------|
| `name`        | Card name                                           |
| `arcana`      | `major` or `minor`                                  |
| `suit`        | `null` (major), `wands`, `cups`, `swords`, `pentacles` |
| `orientation` | `upright` or `reversed`                             |
| `meaning`     | General meaning for that orientation                |

## Tests

```bash
uv run pytest
```

## Project structure

```
app/
├── main.py               # FastAPI app; loads the deck at startup
├── api/v1/router.py      # /v1/api prefix
├── api/v1/routes/tarot.py# GET /tarot-generate
├── core/config.py        # Settings (TAROT_DATA_PATH env var)
├── schemas/tarot.py      # Pydantic models
├── services/tarot.py     # Load YAML, draw a card
└── data/tarot.yaml       # 78 cards with upright/reversed meanings
tests/
gunicorn.conf.py          # Production server settings
deploy/tarot-api.service  # systemd service file
```

## Configuration

- `TAROT_DATA_PATH`: path to another YAML deck file. This setting is optional.

## Data source

The card meanings are short keyword summaries, based on the
[Labyrinthos tarot card meanings list](https://labyrinthos.co/blogs/tarot-card-meanings-list).
