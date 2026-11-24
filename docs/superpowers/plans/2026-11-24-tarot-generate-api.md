# Tarot Generate API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A FastAPI app where `GET /v1/api/tarot-generate` returns one random tarot card (78-card deck, random orientation) and its meaning as JSON.

**Architecture:** Card data lives in `app/data/tarot.yaml`. A service loads it once (cached with `functools.lru_cache`), validates it with Pydantic, and draws a random card. A versioned router exposes the endpoint.

**Tech Stack:** Python 3.12, uv, FastAPI (`fastapi[standard]`), Pydantic v2, pydantic-settings, PyYAML, pytest, httpx.

**Spec:** `docs/superpowers/specs/2026-11-24-tarot-generate-api-design.md`

## Global Constraints

- Package manager: `uv`. Run everything with `uv run`.
- Dev server only: `uv run fastapi dev app/main.py`. No gunicorn/production server.
- No database. Data only in `app/data/tarot.yaml`.
- Endpoint path exactly: `/v1/api/tarot-generate`, method GET.
- Response fields exactly: `name`, `arcana`, `suit`, `orientation`, `meaning`.
- `arcana` is `"major"` or `"minor"`. `suit` is `null` for major, else one of `"wands"`, `"cups"`, `"swords"`, `"pentacles"`. `orientation` is `"upright"` or `"reversed"`.
- No git commits unless the user asks (the user has not asked).

## Review Focus

1. Broken or incomplete YAML (missing card, typo in suit) → app must fail at startup with a clear error, not return bad JSON. Test: data file has exactly 78 unique cards, 22 major, 14 per suit.
2. Repeated calls → must vary (truly random), and both orientations must appear. Test: many calls produce more than one card and both orientations.
3. Meaning must match orientation → `meaning` equals the YAML `upright` text when upright, `reversed` text when reversed. Test with a patched RNG.
4. Wrong method (POST) → 405, not 500. Test.
5. YAML path must not depend on the current working directory → path is built from `Path(__file__)`. Covered by running tests from the project root and the server from the project root.

---

### Task 1: Project setup and YAML data

**Files:**
- Create: `pyproject.toml` (via `uv init --app --no-workspace`), `app/__init__.py`, `app/data/tarot.yaml`, `app/schemas/__init__.py`, `app/schemas/tarot.py`, `tests/__init__.py`, `tests/test_data.py`, `README.md`

**Interfaces:**
- Produces: `app.schemas.tarot.Arcana` (Literal `"major"|"minor"`), `Suit` (Literal of 4 suits), `Orientation` (Literal), `TarotCard(BaseModel)` with `name: str, arcana: Arcana, suit: Suit | None, upright: str, reversed: str`; `TarotDeck(BaseModel)` with `cards: list[TarotCard]`; `TarotReading(BaseModel)` with `name, arcana, suit, orientation: Orientation, meaning: str`.
- YAML shape: top-level `cards:` list of objects with `name, arcana, suit, upright, reversed`.

- [ ] **Step 1:** `uv init`, then `uv add "fastapi[standard]" pyyaml pydantic-settings` and `uv add --dev pytest httpx`. Remove the generated `main.py`.
- [ ] **Step 2:** Research meanings (web) and write all 78 cards to `app/data/tarot.yaml`. Meanings are short keyword phrases.
- [ ] **Step 3: Write test** `tests/test_data.py::test_deck_is_complete`: load YAML into `TarotDeck`; assert `len(cards) == 78`, names unique, 22 with `arcana == "major"` and `suit is None`, 14 per suit, every `upright`/`reversed` non-empty.
- [ ] **Step 4:** Write the schemas. Run `uv run pytest tests/test_data.py -v` → PASS.

### Task 2: Service, router, app

**Files:**
- Create: `app/core/__init__.py`, `app/core/config.py`, `app/services/__init__.py`, `app/services/tarot.py`, `app/api/__init__.py`, `app/api/v1/__init__.py`, `app/api/v1/router.py`, `app/api/v1/routes/__init__.py`, `app/api/v1/routes/tarot.py`, `app/main.py`, `tests/test_tarot_api.py`

**Interfaces:**
- Consumes: Task 1 schemas.
- Produces: `app.core.config.settings` with `app_name: str`, `tarot_data_path: Path` (default `Path(__file__).resolve().parent.parent / "data" / "tarot.yaml"`); `app.services.tarot.load_deck() -> TarotDeck` (`@lru_cache`); `draw_card(rng: random.Random | None = None) -> TarotReading`; `app.main.app`. Deck loads in a FastAPI `lifespan` so bad data fails at startup.

- [ ] **Step 1: Write tests** in `tests/test_tarot_api.py` using `TestClient(app)` as context manager:
  - `test_generate_returns_card`: GET → 200; keys == `{"name","arcana","suit","orientation","meaning"}`; `orientation in {"upright","reversed"}`.
  - `test_meaning_matches_orientation`: call `draw_card(random.Random(0))` and look up the card in `load_deck()`; meaning equals the field named by orientation.
  - `test_generate_is_random`: 200 calls → >1 distinct name and both orientations seen.
  - `test_post_not_allowed`: POST → 405.
- [ ] **Step 2:** Run `uv run pytest -v` → new tests FAIL (import error).
- [ ] **Step 3:** Implement config, service, router (`APIRouter(prefix="/v1/api")`, route `GET /tarot-generate`, `response_model=TarotReading`, `tags=["tarot"]`), and `main.py`.
- [ ] **Step 4:** Run `uv run pytest -v` → all PASS.
- [ ] **Step 5:** Start `uv run fastapi dev app/main.py`, `curl localhost:8000/v1/api/tarot-generate` → JSON card. Stop server. Update README with run and test commands.
