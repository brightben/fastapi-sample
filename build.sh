#!/bin/sh -e
# This file is for local testing build image, it will not use DOCKER BUILDKIT

DOCKER_BUILDKIT=1 docker build -t fastapisample .
ID=$(docker create fastapisample)
rm -rf htmlcov
docker cp $ID:/app/htmlcov htmlcov
docker rm -v $ID
