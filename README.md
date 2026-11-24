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
uv run fastapi dev app/main.py
```

The server runs at http://127.0.0.1:8000. You can see the interactive API docs at http://127.0.0.1:8000/docs.

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
```

## Configuration

- `TAROT_DATA_PATH`: path to another YAML deck file. This setting is optional.

## Data source

The card meanings are short keyword summaries, based on the
[Labyrinthos tarot card meanings list](https://labyrinthos.co/blogs/tarot-card-meanings-list).
