from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .routers import characters, npcs
from .utils import contants as const


app = FastAPI(
    title=const.OPENAPI_TITLE,
    summary=const.OPENAPI_SUMMARY,
    description=const.OPENAPI_DESCRIPTION,
    version=const.OPENAPI_VERSION,
    terms_of_service=const.OPENAPI_VERSION,
    contact=const.OPENAPI_CONTACT,
    license_info=const.OPENAPI_LICENSE_INFO,
)


app.include_router(characters.router)
app.include_router(npcs.router)


@app.get("/status", tags=['ops'], summary='Check API status')
def status():
    return JSONResponse(status_code=200, content={'status': 'UP'})