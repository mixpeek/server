from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional


from files.service import FileTextExtractor
import tika

tika.initVM()

app = FastAPI()


class FileData(BaseModel):
    file: Optional[UploadFile] = None
    file_url: Optional[str] = None


class WebsiteData(BaseModel):
    website: str
    max_depth: int


@app.post("/process/file")
async def process_file(data: FileData):
    if data.file:
        # Read the uploaded file into memory and process it
        file_content = await data.file.read()
        extractor = FileTextExtractor(file=file_content)
    else:
        # Process the file URL as before
        extractor = FileTextExtractor(file_url=data.file_url)
    response, status_code = await extractor.extract_text()
    return JSONResponse(content=response, status_code=status_code)


# from website.service import WebScraper
# from nux import Nux
# from website_scraper import WebScraper

# class WebsiteData(BaseModel):
#     website: str
#     api_key: str
#     max_depth: int
#     loader_id: str

# @app.post('/process/website')
# async def process_website(data: WebsiteData):
#     task = website_handler.delay(
#         website_url=data.website,
#         nux_api_key=data.api_key,
#         max_depth=data.max_depth,
#         loader_id=data.loader_id
#     )

#     return {"task_id": task.id}


# def website_handler(website_url, nux_api_key, max_depth, loader_id):
#     # scrape contents
#     scraper = WebScraper(
#         url=website_url,
#         maxDepth=max_depth
#     )
#     # objects of resources
#     results = scraper.scrapeData()
#     list_of_urls = results['Internal']

#     nux = Nux(api_key=nux_api_key)

#     # send each to nux loader as html (with embed)
#     nux.index_urls(
#         urls=list_of_urls,
#         api_key=nux_api_key,
#         loader_id=loader_id,
#         embed=True,
#         metadata={}
#     )
