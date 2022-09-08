from fastapi import FastAPI
from fastapi import APIRouter
from mangum import Mangum
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version
from fastapi.responses import FileResponse

from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import users

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])


app = FastAPI(docs_url=None, redoc_url=None, openapi_url='/static/hello/openapi.json')


@app.get("/hello/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/hello/swagger-ui-bundle.js",
        swagger_css_url="/static/hello/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/static/hello/{file}")
async def file(file):
    return FileResponse("static/"+file)


@app.get("/file")
async def file():
    return {"message": "A file"}


@app.get("/file/{name}")
async def file(name):
    return {"message": name}


@app.get("/v3/hello")
async def hellov3():
    return {"message": "Hello World v3!"}


@app.get("/v2/hello")
async def hellov2():
    return {"message": "Hello World v2!"}

app.include_router(router, prefix="/api/v1")

handler = Mangum(app)
