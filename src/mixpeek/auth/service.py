from fastapi import Depends, HTTPException, Header, Request
from organization.service import OrganizationSyncService
from typing import Optional

from config import auth_off

from fastapi import FastAPI, HTTPException
from typing import Optional


def get_index_id(
    request: Request,
    # Receive the entire Authorization header
    Authorization: Optional[str] = Header(None),
    # Make it optional):
    index_id: Optional[str] = Header(None, description="filter by organization"),
):
    # if user supplied scope in params, no index_id aneeded
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    # Split the header to extract the token
    try:
        scheme, api_key = Authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(
            status_code=401, detail="Invalid authorization header format"
        )

    try:
        index_id, organization = OrganizationSyncService().get_index_ids(
            api_key, index_id
        )
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid API key")

    if not index_id:
        raise HTTPException(status_code=400, detail="Index ID not found")

    request.index_id = index_id
    request.api_key = api_key

    return index_id
