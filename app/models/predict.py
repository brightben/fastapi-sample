from pydantic import BaseModel, Field
from typing import Optional, List, Union, Literal

from core.fastapisample_config import (MAC_NULL_MATCH_PATTERN)


class userReqModel(BaseModel):
    """ User Request Model """
    device_name: str = Field(pattern=MAC_NULL_MATCH_PATTERN)
    org_id: Optional[int] = None
    text: str

    class Config:
        json_schema_extra = {
            "example": {
                "device_name": "MAC-aa-aa-aa-aa-aa-aa",
                "org_id": 5,
                "text": "what is your name?"
            }
        }


class AnswerResModel(BaseModel):
    """ User Answer Response Model """
    text: Optional[str] = ""


class userReqResModel(BaseModel):
    """ User Response Model """
    answer: AnswerResModel = {}

    class Config:
        json_schema_extra = {
            "example": {
                "answer": {
                    "text": "My name is Josh."
                }
            }
        }


class userResBasicModel(BaseModel):
    """ User Response Basic Model """
    text: Optional[str] = ""
    aaa: bool
    bbb: Union[int, None]
    ccc: Literal['test', 'test2', 'test3']
    ddd: str


class userResModel(BaseModel):
    """ User Response Model """
    answer: List[userResBasicModel] = {}

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class userUpdateReqModel(BaseModel):
    """ User Update Request Model """
    device_name: str = Field(pattern=MAC_NULL_MATCH_PATTERN)
    org_id: Optional[int] = None
    text: str

    class Config:
        json_schema_extra = {
            "example": {
                "device_name": "MAC-aa-aa-aa-aa-aa-aa",
                "org_id": 5,
                "text": "what is your name?"
            }
        }


class userDeleteReqModel(BaseModel):
    """ User Delete Request Model """
    user_id_list: List[int]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id_list": [1, 2, 32]
            }
        }
