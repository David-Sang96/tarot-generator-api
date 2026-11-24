import random
from functools import lru_cache
from typing import get_args

import yaml

from app.core.config import settings
from app.schemas.tarot import Orientation, TarotDeck, TarotReading

_ORIENTATIONS: tuple[Orientation, ...] = get_args(Orientation)
_rng = random.SystemRandom()


@lru_cache(maxsize=1)
def load_deck() -> TarotDeck:
    """Read and validate the YAML deck once, then keep it in memory."""
    raw = yaml.safe_load(settings.tarot_data_path.read_text(encoding="utf-8"))
    return TarotDeck.model_validate(raw)


def draw_card(rng: random.Random | None = None) -> TarotReading:
    """Pick a random card and a random orientation."""
    rng = rng or _rng
    card = rng.choice(load_deck().cards)
    orientation = rng.choice(_ORIENTATIONS)
    return TarotReading(
        name=card.name,
        arcana=card.arcana,
        suit=card.suit,
        orientation=orientation,
        meaning=getattr(card, orientation),
    )
