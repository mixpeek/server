from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, Union, cast

from auth.service import get_index_id
from db.model import PaginationParams
from _exceptions import NotFoundError

from .model import CreateOrgRequest, TrustedOrgResponse, OrganizationUpdateRequest
from .service import OrganizationSyncService
from fastapi import Request, Response, status

from config import mixpeek_admin_token

router = APIRouter()


@router.post("/", include_in_schema=False)
async def create_organization(request: Request, Authorization: str = Header(None)):
    if Authorization != mixpeek_admin_token:
        raise NotFoundError("Invalid admin token")

    payload = await request.json()

    if payload.get("user", {}).get("email", None) is None:
        raise NotFoundError("Email is required")

    org_service = OrganizationSyncService()
    return org_service.create_organization(email=payload["user"]["email"])


@router.put("/", response_model=TrustedOrgResponse, include_in_schema=False)
def update_organization(
    updates: OrganizationUpdateRequest, index_id: str = Depends(get_index_id)
):
    service = OrganizationSyncService()
    updates_dict = updates.dict(exclude_unset=True)
    return service.update_organization(index_id, updates_dict)


@router.get("/", response_model=TrustedOrgResponse, include_in_schema=False)
def get_organization(index_id: str = Depends(get_index_id)):
    service = OrganizationSyncService()
    return service.get_organization(index_id)


# @router.post("/secrets")
# def add_secret(secret: SecretRequest, index_id: str = Depends(get_index_id)):
#     organization_service = OrganizationSyncService()

#     try:
#         organization_service.add_secret(index_id, secret.name, secret.value)
#         return {"message": "Secret added successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @router.delete("/secrets")
# def delete_secret(secret_name: str, index_id: str = Depends(get_index_id)):
#     organization_service = OrganizationSyncService()

#     try:
#         organization_service.delete_secret(index_id, secret_name)
#         return {"message": "Secret deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
