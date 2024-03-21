from fastapi import APIRouter, HTTPException, Body, Depends, Request
import json

from .model import ConnectionInformation
from .service import ListenerAsyncService

router = APIRouter()


@router.post("/{provider}")
async def receive_payload(request: Request):
    listener_service = ListenerAsyncService(request.index_id)
    obj = await request.json()
    listener_service.insert(obj["record"])

    return {"message": "received"}
