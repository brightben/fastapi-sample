FROM python:3.8.16 AS build-stage

# Copy Fastapi sample src code
WORKDIR /app
ADD . .

# Install requirement and flake8
RUN pip install -r requirements.txt
RUN flake8 --max-line-length=160 $(find . -not \( -path ./.env -prune \) -not \( -path ./app/tests -prune \) -not \( -path ./app/core -prune \) -not \( -path ./build -prune \) -type f -name \*.py)
RUN cd app && ENV_FOR_DYNACONF=testing ../test.sh

# Build Fastapi sample with pyinstaller
RUN pyinstaller -F \
                --onefile --additional-hooks-dir hooks/ \
                --hidden-import uvicorn \
                --hidden-import uvicorn.logging \
                --hidden-import uvicorn.loops.auto \
                --hidden-import uvicorn.loops.asyncio \
                --hidden-import uvicorn.loops.uvloop \
                --hidden-import uvicorn.loops \
                --hidden-import uvicorn.protocols \
                --hidden-import uvicorn.protocols.http \
                --hidden-import uvicorn.protocols.http.auto \
                --hidden-import uvicorn.protocols.http.h11_impl \
                --hidden-import uvicorn.protocols.http.httptools_impl \
                --hidden-import uvicorn.protocols.websockets \
                --hidden-import uvicorn.protocols.websockets.auto \
                --hidden-import uvicorn.protocols.websockets.wsproto_impl \
                --hidden-import uvicorn.protocols.websockets_impl \
                --hidden-import uvicorn.lifespan \
                --hidden-import uvicorn.lifespan.on \
                --hidden-import uvicorn.lifespan.off \
                --hidden-import tiktoken_ext.openai_public \
                --hidden-import tiktoken_ext \
                -n fastapisample --distpath . app/fastapisample_main.py

FROM python:3.8-slim-bullseye AS production-stage

# Create app directory
WORKDIR /app
ADD run.sh .
RUN ["chmod", "+x", "run.sh"]

# Copy Fastapi Sample binary code
COPY --from=build-stage /app/fastapisample /app
ADD app/config/static_config.json config/static_config.json

# Copy coverage report
COPY --from=build-stage /app/app/htmlcov /app/htmlcov

EXPOSE 55688
CMD ["./run.sh"]
