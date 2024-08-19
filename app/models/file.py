from pydantic import BaseModel
from typing import List


class imageDelModel(BaseModel):
    """ Image delete data model """
    image_list: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "image_list": [
                    "a.png",
                    "b.png"
                ]
            }
        }
