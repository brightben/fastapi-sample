import logging

from fastapi import HTTPException, Response, BackgroundTasks

from app_lib.custom_api_router import APIRouter
from app_lib.func_utility import background_task_sample
from core.config import settings
from models.predict import (userReqModel, userReqResModel, userResModel, userUpdateReqModel, userDeleteReqModel)


# Setting Logger
LOGGER = logging.getLogger(__name__)

router = APIRouter()


@router.post("", status_code=201, response_model=userReqResModel)
async def add_user_chat(
    *,
    background_tasks: BackgroundTasks,
    content: userReqModel
):
    """
    Description: Add user
    """
    input_data = content.model_dump(by_alias=True)
    LOGGER.warning(f"Add user data, input data: {input_data}")
    LOGGER.warning(f"Sample test setting config data: {settings['SLACK_SERVER_URL']}")

    # Check input data here
    if 'name' not in input_data.get('text'):
        error_detail = f"Input text error, input_data: {input_data}"
        LOGGER.error(error_detail)
        raise HTTPException(status_code=400, detail=error_detail)

    res_data = {
        'answer': {
            'text': 'your answer here'
        }
    }

    # Add background task running after return
    background_tasks.add_task(background_task_sample, 'input_aaa', 'input_bbb', 'input_ccc')

    return res_data


@router.get("", response_model=userResModel)
async def get_user_data():
    """
    Description: Get data
    """
    LOGGER.info("User get data")
    res_data = {
        "answer": [
            {
                "text": "lalalalalal",
                "aaa": True,
                "bbb": 5,
                "ccc": "test2",
                "ddd": "yolo"
            }
        ]
    }

    return res_data


@router.put("/{id}", status_code=201, response_model=userUpdateReqModel)
async def update_user_data(
    id: str,
    content: userUpdateReqModel
):
    """
    Description: Update data
    """
    input_data = content.model_dump(by_alias=True)
    LOGGER.warning(f"Update user data, id: {id}, input data: {input_data}")
    return content


@router.delete(
    "",
    response_class=Response,
    responses={
        204: {"description": "User deleted success"},
        400: {"description": "User deleted error"},
        404: {"description": "User not found error"},
    }
)
async def delete_user_data(
    content: userDeleteReqModel
):
    """ Delete device ngfw in db """
    input_data = content.model_dump(by_alias=True)
    LOGGER.warning(f"Delete user data, input data: {input_data}")
    if 2 not in input_data.get('user_id_list'):
        error_detail = f"Input text error, input_data: {input_data}"
        LOGGER.error(error_detail)
        return Response(status_code=404)

    if 1 not in input_data.get('user_id_list'):
        error_detail = f"Input text error, input_data: {input_data}"
        LOGGER.error(error_detail)
        return Response(status_code=400)

    return Response(status_code=204)
