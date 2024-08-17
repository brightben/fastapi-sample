import os
import logging
import secrets

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


# Setting Logger
LOGGER = logging.getLogger(__name__)
# Initialize Login security
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    """ Check docs login username password is correct """
    username = os.getenv('API_USER', "hello")
    password = os.getenv('API_PASS', "hellotestingfastapi")
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
