#!/bin/sh -e

trap "trap - TERM && kill -- -$$" TERM

service_run() {
  /app/fastapisample &
  wait
}

service_run
