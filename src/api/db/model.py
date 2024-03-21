from pydantic import BaseModel
from typing import Optional


class PaginationParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
