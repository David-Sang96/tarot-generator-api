from typing import Literal, get_args

from pydantic import BaseModel, ConfigDict, Field, model_validator

Arcana = Literal["major", "minor"]
Suit = Literal["wands", "cups", "swords", "pentacles"]
Orientation = Literal["upright", "reversed"]

DECK_SIZE = 78
MAJOR_COUNT = 22
SUIT_SIZE = 14


class TarotCard(BaseModel):
    """One card as stored in the YAML data file."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    name: str = Field(min_length=1)
    arcana: Arcana
    suit: Suit | None = None
    upright: str = Field(min_length=1)
    reversed: str = Field(min_length=1)

    @model_validator(mode="after")
    def check_suit_matches_arcana(self) -> "TarotCard":
        if self.arcana == "major" and self.suit is not None:
            raise ValueError(f"{self.name}: major arcana cards must not have a suit")
        if self.arcana == "minor" and self.suit is None:
            raise ValueError(f"{self.name}: minor arcana cards must have a suit")
        return self


class TarotDeck(BaseModel):
    """The whole deck loaded from YAML."""

    cards: list[TarotCard] = Field(min_length=1)

    @model_validator(mode="after")
    def check_full_deck(self) -> "TarotDeck":
        names = [c.name for c in self.cards]
        duplicates = sorted({n for n in names if names.count(n) > 1})
        if duplicates:
            raise ValueError(f"Duplicate cards in deck: {', '.join(duplicates)}")
        if len(self.cards) != DECK_SIZE:
            raise ValueError(f"Deck must have {DECK_SIZE} cards, found {len(self.cards)}")
        major = sum(1 for c in self.cards if c.arcana == "major")
        if major != MAJOR_COUNT:
            raise ValueError(f"Deck must have {MAJOR_COUNT} major arcana cards, found {major}")
        for suit in get_args(Suit):
            count = sum(1 for c in self.cards if c.suit == suit)
            if count != SUIT_SIZE:
                raise ValueError(f"Suit {suit} must have {SUIT_SIZE} cards, found {count}")
        return self


class TarotReading(BaseModel):
    """API response: one drawn card and its meaning."""

    name: str
    arcana: Arcana
    suit: Suit | None
    orientation: Orientation
    meaning: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "The Star",
                    "arcana": "major",
                    "suit": None,
                    "orientation": "upright",
                    "meaning": "Hope, faith, rejuvenation.",
                }
            ]
        }
    )
