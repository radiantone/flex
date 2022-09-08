from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

router = APIRouter()


@router.get("/")
async def get_users():
    return {"message": "Users!"}