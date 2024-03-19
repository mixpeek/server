from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uvicorn

from website.service import WebScraper
from website.model import WebsiteData

from package.model import PackageData
from package.service import PackageManager

from file.service import ParseHandler
from file.model import ParseFileRequest

from _exceptions import APIError, BadRequestError, NotFoundError, InternalServerError


app = FastAPI()


class ResponseData(BaseModel):
    text: Optional[str] = Field(None, description="Extracted text from the file")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata of the file")


class ApiResponse(BaseModel):
    status: str = Field(..., description="Status of the request")
    message: str = Field(..., description="Detailed message")
    data: Optional[ResponseData] = Field(None, description="Data of the response")


@app.post("/file")
async def parse_file(
    parser_request: ParseFileRequest,
    should_chunk: Optional[bool] = True,
):
    parse_handler = ParseHandler(parser_request.file_url)
    try:
        return await parse_handler.parse(should_chunk)
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)


@app.post("/website")
async def process_website(data: WebsiteData):
    scraper = WebScraper(data.website, data.max_depth)
    response, status_code = await scraper.scrapeData()
    return JSONResponse(content=response, status_code=status_code)


@app.post("/package", response_model=ApiResponse)
async def process_request(data: PackageData):
    processor = PackageManager()
    response, status_code = await processor.process(data.model_dump())
    return JSONResponse(content=response, status_code=status_code)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
