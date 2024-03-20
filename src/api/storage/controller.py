from fastapi import APIRouter, HTTPException, Body, Depends, Request

router = APIRouter()


@router.post("/")
async def insert_into_db(request: Request, data: dict = Body(...)):
    return {"status": "ok"}
