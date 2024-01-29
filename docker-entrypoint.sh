#!/bin/bash

set -e

export PYTHONUNBUFFERED=1

. ~/.bashrc

case "$1" in
    web)
        echo "Running App ..."
        exec uvicorn src.main:app --host 0.0.0.0 --port 8000
    ;;
    *)
        exec $@
    ;;
esac
