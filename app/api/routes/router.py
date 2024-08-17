from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from api.auth.auth_handler import get_current_username
from api.routes import (predict)
from core.config import settings

api_router = APIRouter()


@api_router.get("/docs", include_in_schema=False)
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@api_router.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title="FastAPI", routes=api_router.routes)


@api_router.get("/")
async def root():
    """ Welcome Fastapi Sample manager """
    welcome_msg = 'Welcome Fastapi Sample Manager. Running version: ' + settings['API']['GIT_TAG'] + '. Enjoy!'
    return {'message': welcome_msg}

api_router.include_router(predict.router, tags=["sample api"], prefix="/fastapisample/predict")
