from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .routers import characters


description = """
## TBD
"""

app = FastAPI(
    title="3D&T Victory Character Creator API",
    summary="An API for creating/storing 3D&T characters",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Luis Yamada",
        "url": "https://www.linkedin.com/in/luis-yamada/",
        "email": "luishm.yamada@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


app.include_router(characters.router)


@app.get("/status", tags=['ops'], summary='Check API status')
def status():
    return JSONResponse(status_code=200, content={'status': 'UP'})