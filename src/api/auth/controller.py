from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def test():
    # Logic to list all stages
    return {"message": "ok"}
