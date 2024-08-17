import logging
import signal
import sys
import time

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn

from api.routes.router import api_router
from app_lib.func_utility import setup_system_initialize
from core.config import settings
from app_lib import clogging
from app_lib.unbuffered_io import UnbufferedIO

# Setting Logger
LOGGER = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": "sample api",
        "description": "The api for handling sample function."
    }
]


tags_metadata = sorted(tags_metadata, key=lambda row: (row['name']))


def get_app(config, lifespan) -> FastAPI:
    """ Create fastApi app server """

    api_version = 'v0.0.0'
    if 'API' in config:
        if 'GIT_TAG' in config['API']:
            api_version = config['API']['GIT_TAG']

    fast_app = FastAPI(
        title="Sample Manager",
        description="This is a very fancy project. Apply Fastapi Sample API.",
        version=api_version,
        openapi_tags=tags_metadata,
        debug=True,
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan
    )
    # Enable CORS
    origins = [
        "*",
    ]

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fast_app.include_router(api_router)

    return fast_app


def signal_handler(signum, frame):
    """ Signal Handler """
    # ignore additional signals to prevent shutdown from being interrupted
    signal.signal(signum, signal.SIG_IGN)
    sig_map = {
        2: 'SIGINT',
        15: 'SIGTERM',
    }
    if signum in sig_map:
        sig_str = sig_map[signum]
    else:
        sig_str = str(signum)
    LOGGER.info('Receive signal %s', sig_str)
    sys.exit(0)


def main():
    """ Sample main function """

    # Log part, default log will be INFO mode
    clogging.logConfig()
    # Add stderr in IO for container using
    sys.stderr = UnbufferedIO(sys.stderr)

    signal.signal(signal.SIGINT, signal_handler)  # ctrl-c
    signal.signal(signal.SIGTERM, signal_handler)  # k8s delete pod

    LOGGER.debug(settings.keys())

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        LOGGER.info("Fastapi Sample Startup procedure")
        # Load system initialize data
        setup_system_initialize()
        yield

    # Start fastAPI Server
    app = get_app(settings, lifespan)

    # Run Prometheus Client
    Instrumentator().instrument(app).expose(app)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        if process_time >= 2000:
            LOGGER.info(f"{request.method} {request.url.path} cost long time, completed_in={formatted_process_time}ms status_code={response.status_code}")
        else:
            LOGGER.debug(f"{request.method} {request.url.path} completed_in={formatted_process_time}ms status_code={response.status_code}")

        return response

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        LOGGER.error(f"OMG! The client sent invalid data!: {exc}")
        LOGGER.error("Request Body:")
        LOGGER.error(f"{exc.body}")
        return await request_validation_exception_handler(request, exc)

    uvicorn.run(
        app,
        host=settings['API']['IP'],
        port=settings['API']['PORT']
    )


if __name__ == '__main__':
    main()
