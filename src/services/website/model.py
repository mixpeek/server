from pydantic import BaseModel


class WebsiteData(BaseModel):
    website: str
    max_depth: int
