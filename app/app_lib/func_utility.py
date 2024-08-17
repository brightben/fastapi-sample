import json
import logging
from decimal import Decimal

# Setting Logger
LOGGER = logging.getLogger(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def setup_system_initialize():
    """ Setup Sample Fastapi initialized status """
    # Do what you want here at the start of your program
    return


def background_task_sample(input_a: str, input_b: str, input_c: str):
    """ Description """
    LOGGER.warning(f"In background task, input a: {input_a}, input b: {input_b}, input c: {input_c}")
    return


def value_serializer(m):
    return json.dumps(m).encode()


def dict_to_str(input_dict: dict) -> str:
    """ Transfer dict to string """
    return json.dumps(input_dict, cls=JSONEncoder)


def str_to_dict(input_str: str) -> dict:
    """ Transfer string to dict """
    return json.loads(input_str)
