from fastapi import APIRouter, UploadFile, Body, File

from .model import FileType, CollectionModel, CollectionResponse
from .service import detect_filetype, CollectionService

router = APIRouter()


@router.post("/detect-filetype", response_model=FileType)
async def detect_file(file: UploadFile = File(...)):
    contents = await file.read()
    return detect_filetype(contents)


@router.post("/collection", response_model=CollectionResponse)
async def create_collection(collection: CollectionModel = Body(...)):
    collection_dict = CollectionService.create_collection(collection)
    return collection_dict


@router.post("/", response_model=CollectionResponse)
async def create_collection(collection: CollectionModel = Body(...)):
    pass
