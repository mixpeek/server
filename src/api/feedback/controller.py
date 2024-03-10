from fastapi import APIRouter, HTTPException, Body, Depends, Request

from .model import FeedbackSchema

# from auth.service import get_index_id

router = APIRouter()


@router.get("/")
def collect_feedback(
    # index_id: str = Depends(get_index_id),
    # feedback: FeedbackSchema = Body(...),
):
    return {"status": "ok"}
