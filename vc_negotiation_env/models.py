from pydantic import BaseModel
from typing import Optional, List, Dict

class Action(BaseModel):
    action_type: str  # "ask", "offer", "accept", "walkaway"
    message: Optional[str] = None
    valuation: Optional[float] = None
    equity: Optional[float] = None

class Observation(BaseModel):
    founder_message: str
    round_number: int
    deal_closed: bool
    founder_walked: bool
    rewards: Dict[str, float] = {}

class DealState(BaseModel):
    founder_target_valuation: float
    founder_min_valuation: float
    founder_max_equity: float
    competing_offer: Optional[float] = None
    current_round: int = 0
    max_rounds: int = 6
    deal_closed: bool = False
    founder_walked: bool = False
    offers_made: List[dict] = []