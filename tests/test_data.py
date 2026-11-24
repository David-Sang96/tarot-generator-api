from collections import Counter

import pytest
import yaml
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.tarot import TarotCard, TarotDeck


def test_deck_is_complete():
    raw = yaml.safe_load(settings.tarot_data_path.read_text(encoding="utf-8"))
    deck = TarotDeck.model_validate(raw)

    assert len(deck.cards) == 78
    assert len({c.name for c in deck.cards}) == 78

    major = [c for c in deck.cards if c.arcana == "major"]
    assert len(major) == 22
    assert all(c.suit is None for c in major)

    suits = Counter(c.suit for c in deck.cards if c.arcana == "minor")
    assert suits == {"wands": 14, "cups": 14, "swords": 14, "pentacles": 14}

    assert all(c.upright.strip() and c.reversed.strip() for c in deck.cards)


def _full_deck_data() -> dict:
    return yaml.safe_load(settings.tarot_data_path.read_text(encoding="utf-8"))


def test_card_rejects_blank_meaning():
    with pytest.raises(ValidationError):
        TarotCard(name="The Fool", arcana="major", upright="   ", reversed="Recklessness.")


def test_deck_rejects_missing_card():
    data = _full_deck_data()
    data["cards"] = data["cards"][:-1]
    with pytest.raises(ValidationError, match="78"):
        TarotDeck.model_validate(data)


def test_deck_rejects_duplicate_card():
    data = _full_deck_data()
    data["cards"][-1] = data["cards"][0]
    with pytest.raises(ValidationError, match="[Dd]uplicate"):
        TarotDeck.model_validate(data)
