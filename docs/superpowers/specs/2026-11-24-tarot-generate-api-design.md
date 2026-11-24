# Tarot Generate API — Short Design

**Status:** Approved by user on 2026-11-24.

## Intent
A small Python API. A GET request to `/v1/api/tarot-generate` returns one random
tarot card and its general meaning as simple JSON.

## Goals
- Full 78-card deck: 22 Major Arcana + 56 Minor Arcana (Wands, Cups, Swords, Pentacles).
- Each draw picks a random card and a random orientation (upright or reversed).
- Card data and meanings live in one YAML file. Meanings are researched from public sources.

## Non-goals
- No database.
- No production web server. Use the FastAPI built-in dev server (`fastapi dev`).

## Constraints
- `uv` for package management.
- FastAPI web framework, best-practice folder layout.
- Project folder: `/home/david/Desktop/tarot-card-generation-api`.

## Approaches
1. **YAML loaded once at startup, kept in memory (chosen).** Fast and simple. The data is small and never changes while running.
2. YAML read on every request. Simpler, but wastes work on each call.
3. Data hard-coded in Python. Rejected: the user asked for YAML.

## Design
- `app/main.py` — creates the FastAPI app, includes the v1 router.
- `app/api/v1/routes/tarot.py` — `GET /v1/api/tarot-generate`.
- `app/schemas/tarot.py` — Pydantic models for the YAML card and the response.
- `app/services/tarot.py` — loads the YAML (cached) and draws a card.
- `app/core/config.py` — settings, such as the YAML path.
- `app/data/tarot.yaml` — 78 cards: `name`, `arcana`, `suit`, `upright`, `reversed`.
- `tests/` — pytest tests for the endpoint and the data file.

Response example:
```json
{"name": "The Star", "arcana": "major", "suit": null,
 "orientation": "upright", "meaning": "Hope, renewal, inspiration."}
```

## Left to the builder
- Exact wording of meanings (short keyword phrases).
- Minor details of the settings and test layout.
