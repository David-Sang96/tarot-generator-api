from fastapi import APIRouter

from app.schemas.tarot import TarotReading
from app.services.tarot import draw_card

router = APIRouter(tags=["tarot"])


@router.get("/tarot-generate", response_model=TarotReading)
def generate_tarot_card() -> TarotReading:
    """Draw one random tarot card (upright or reversed) with its general meaning."""
    return draw_card()
