from pydantic import BaseModel, confloat
from typing import Optional, List

class FeedbackSchema(BaseModel):
    run_id: str
    block_id: str
    response: dict
    feedback: dict
    rating: Optional[confloat(le=100)]
    interactions: Optional[List[dict]]