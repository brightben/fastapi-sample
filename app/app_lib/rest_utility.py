import json
import logging
import requests
from requests.auth import HTTPBasicAuth

from fastapi import HTTPException

logger = logging.getLogger(__name__)


def send_restful(url, req_type='get', payload=None, header=None, time_out=40, verify=False,
                 auth_method: str = None, username: str = None, password: str = None):
    """_summary_

    Args:
        url (_type_): _description_
        req_type (str, optional): _description_. Defaults to 'get'.
        payload (_type_, optional): _description_. Defaults to None.
        header (_type_, optional): _description_. Defaults to None.
        time_out (int, optional): _description_. Defaults to 40.
        verify (bool, optional): _description_. Defaults to False.
        auth_method (str, optional): Can be basic_auth or others. Defaults to None.
        username (str, optional): _description_. Defaults to None.
        password (str, optional): _description_. Defaults to None.

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    logger.debug(f'Payload: {payload}')
    logger.debug(f'Send to {url!r}')
    auth = None
    try:
        # 1. Check auth method
        if auth_method == 'basic_auth':
            if username and password:
                auth = HTTPBasicAuth(username, password)
        # 2. Check request type
        req_type = req_type.lower()
        method_list = ['get', 'post', 'put', 'delete']
        if req_type not in method_list:
            logger.error(f'Send restful type error, Send to {url!r}, Request type: {req_type}')
            raise HTTPException(status_code=400, detail='Send restful type error.')
        # 3. Send request
        if req_type == 'get':
            res = requests.get(url, headers=header, timeout=time_out, verify=verify, auth=auth)
        elif req_type == 'post':
            res = requests.post(url, json=payload, headers=header, timeout=time_out, verify=verify, auth=auth)
        elif req_type == 'put':
            res = requests.put(url, json=payload, headers=header, timeout=time_out, verify=verify, auth=auth)
        elif req_type == 'delete':
            res = requests.delete(url, json=payload, headers=header, timeout=time_out, verify=verify, auth=auth)
    except requests.exceptions.Timeout as exc:
        logger.error(f'Send restful timeout, Send to {exc.request.url!r}, Request type: {req_type}')
        logger.error(f'Timeout: {time_out}')
        logger.error(f'Detail - {exc!r}')
        if payload is not None:
            logger.error('Error data:')
            logger.error(payload)
        raise HTTPException(status_code=400, detail='Send restful timeout.')
    except requests.exceptions.ConnectionError as exc:
        logger.error(f'HTTP connection error, Send to {exc.request.url!r}, Request type: {req_type}')
        logger.error(f'Detail - {exc!r}')
        raise HTTPException(status_code=400, detail='Http Connection Error')
    logger.debug(f'Response code: {res.status_code}')
    logger.debug(f'Response text: {res.text}')
    if res.status_code < 210:
        try:
            return res.json(), res.status_code
        except json.decoder.JSONDecodeError:
            return res.text, res.status_code
    else:
        return "", res.status_code


def send_restful_wo_fastapi(url, req_type='get', payload=None, header=None, time_out=40, verify=False):
    logger.debug(f'Payload: {payload}')
    logger.debug(f'Send to {url!r}')
    try:
        req_type = req_type.lower()
        method_list = ['get', 'post', 'put', 'delete']
        if req_type not in method_list:
            logger.error(f'Send restful type error, Send to {url!r}, Request type: {req_type}')
            return "Send restful method error!", 403
        if req_type == 'get':
            res = requests.get(url, headers=header, timeout=time_out, verify=verify)
        elif req_type == 'post':
            res = requests.post(url, json=payload, headers=header, timeout=time_out, verify=verify)
        elif req_type == 'put':
            res = requests.put(url, json=payload, headers=header, timeout=time_out, verify=verify)
        elif req_type == 'delete':
            res = requests.delete(url, json=payload, headers=header, timeout=time_out, verify=verify)
    except requests.exceptions.Timeout as exc:
        logger.error(f'Send restful timeout, Send to {exc.request.url!r}, Request type: {req_type}')
        logger.error(f'Timeout: {time_out}')
        logger.error(f'Detail - {exc!r}')
        if payload is not None:
            logger.error('Error data:')
            logger.error(payload)
        return "Send restful timeout!", 400
    except requests.exceptions.ConnectionError as exc:
        logger.error(f'HTTP connection error, Send to {exc.request.url!r}, Request type: {req_type}')
        logger.error(f'Detail - {exc!r}')
        return "Http Connection Error", 400
    logger.debug(f'Response code: {res.status_code}')
    logger.debug(f'Response text: {res.text}')

    try:
        return res.json(), res.status_code
    except json.decoder.JSONDecodeError:
        return res.text, res.status_code
