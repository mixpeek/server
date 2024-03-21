from fastapi import Header, Request
from organization.service import OrganizationSyncService
from typing import Optional

from _exceptions import BadRequestError, NotFoundError


def get_index_id(
    request: Request,
    # Receive the entire Authorization header
    Authorization: Optional[str] = Header(None),
    # Make it optional):
    index_id: Optional[str] = Header(None, description="filter by organization"),
):
    # if user supplied scope in params, no index_id aneeded
    if Authorization is None:
        raise BadRequestError(error="Authorization header is missing")

    # Split the header to extract the token
    try:
        scheme, api_key = Authorization.split()
        if scheme.lower() != "bearer":
            raise BadRequestError(error="Invalid authentication scheme")
    except ValueError:
        raise BadRequestError(error="Invalid authorization header format")

    try:
        index_id, organization = OrganizationSyncService().get_index_ids(
            api_key, index_id
        )
    except Exception as e:
        raise NotFoundError(error="Invalid API key")

    if not index_id:
        raise NotFoundError(error="Index ID not found")

    request.index_id = index_id

    return index_id
