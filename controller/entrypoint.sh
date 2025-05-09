#!/bin/sh


trap 'kill -TERM $PID' TERM INT

poetry run uvicorn src.controller.main:app --host 0.0.0.0 --port 8060 --reload &

PID=$!
wait $PID
