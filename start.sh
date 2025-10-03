#!/usr/bin/env bash
set -euo pipefail

PORT=${PORT:-8000}
exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:${PORT} api:app
