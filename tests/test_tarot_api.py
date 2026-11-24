import random

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.tarot import draw_card, load_deck

URL = "/v1/api/tarot-generate"


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_generate_returns_card(client):
    resp = client.get(URL)
    assert resp.status_code == 200
    body = resp.json()
    assert set(body) == {"name", "arcana", "suit", "orientation", "meaning"}
    assert body["orientation"] in {"upright", "reversed"}
    assert body["arcana"] in {"major", "minor"}


def test_meaning_matches_orientation():
    cards = {c.name: c for c in load_deck().cards}
    for seed in range(20):
        reading = draw_card(random.Random(seed))
        card = cards[reading.name]
        assert reading.meaning == getattr(card, reading.orientation)
        assert reading.arcana == card.arcana
        assert reading.suit == card.suit


def test_generate_is_random(client):
    bodies = [client.get(URL).json() for _ in range(200)]
    assert len({b["name"] for b in bodies}) > 1
    assert {b["orientation"] for b in bodies} == {"upright", "reversed"}


def test_post_not_allowed(client):
    assert client.post(URL).status_code == 405
