from fastapi import FastAPI
from fastapi import APIRouter
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version

import users

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])


app = FastAPI()


@app.get("/hello")
@version(1, 0)
async def hellov1():
    return {"message": "Hello World v1!"}


@app.get("/hello")
@version(2, 0)
async def hellov2():
    return {"message": "Hello World v2!"}

app.include_router(router, prefix="/api/v1")

app = VersionedFastAPI(app)
handler = Mangum(app)
