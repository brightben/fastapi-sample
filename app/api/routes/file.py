import os
import logging

from fastapi import UploadFile, File, HTTPException, Response
from fastapi.responses import FileResponse
from typing import List

from app_lib.custom_api_router import APIRouter
from app_lib.file_utility import FileUtility
from core.fastapisample_config import (FILE_SAVED_FOLDER)
from models.file import imageDelModel

# Setting Logger
LOGGER = logging.getLogger(__name__)

router = APIRouter()


@router.post("", status_code=201)
async def add_image_sync(
    images: List[UploadFile] = File(...)
):
    """ Upload image list """
    file_obj = FileUtility(FILE_SAVED_FOLDER)
    res_data = await file_obj.save_files(images)

    return {"filename": res_data}


@router.get("/{image_name}", status_code=200)
async def get_image_sync(image_name: str):
    """ Get image """
    image_url = f"{FILE_SAVED_FOLDER}{image_name}"
    if os.path.exists(image_url):
        return FileResponse(image_url)
    else:
        LOGGER.error(f"File is not exist, please check. Full file path: {image_url}")
        raise HTTPException(status_code=400, detail='Image url error.')


@router.delete(
    "",
    response_class=Response,
    responses={
        204: {"description": "Image delete success"},
        400: {"description": "Image delete failed"},
        404: {"description": "Image delete failed or not found"},
    }
)
async def delete_image_async(content: imageDelModel):
    """ Delete specific image """
    input_data = content.model_dump(by_alias=True)
    LOGGER.warning(f"Delete image, image name list: {input_data['image_list']}")

    file_obj = FileUtility(FILE_SAVED_FOLDER)
    await file_obj.delete_files(input_data['image_list'])

    return Response(status_code=204)
