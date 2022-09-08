from fastapi import FastAPI
from fastapi import APIRouter
from mangum import Mangum
from fastapi.responses import FileResponse

from models import Asset, Bundle, Availability
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
router = APIRouter()


app = FastAPI(docs_url=None, redoc_url=None, openapi_url='/static/catalog/openapi.json')


@app.get("/catalog/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/catalog/swagger-ui-bundle.js",
        swagger_css_url="/static/catalog/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/static/catalog/{file}")
async def file(file):
    return FileResponse("static/"+file)


@app.post("/asset/", response_model=Asset)
async def post_asset(asset: Asset) -> Asset:
    asset.save()

    return asset


@app.get("/asset/{assetid}", response_model=Asset)
async def get_asset(assetid) -> Asset:

    results = Asset.find({'id': assetid}, response=True)

    asset: Asset = results.first()
    return asset

handler = Mangum(app)
