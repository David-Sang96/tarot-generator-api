"""Gunicorn settings for running the API in production.

Start the server with:
    uv run gunicorn app.main:app

Gunicorn reads this file by default. It manages worker processes,
and each worker runs the FastAPI app with Uvicorn.

Each value can be changed with an environment variable (see below).
"""

import multiprocessing
import os

# Address and port to listen on. 0.0.0.0 accepts connections from other computers.
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")

# Number of worker processes. This app is small, so one worker per CPU core
# (at most 4) is enough by default.
workers = int(os.getenv("GUNICORN_WORKERS", min(multiprocessing.cpu_count(), 4)))

# Run the async FastAPI app with Uvicorn inside each Gunicorn worker.
worker_class = "uvicorn_worker.UvicornWorker"

# Restart a worker if it does not answer for this many seconds.
timeout = int(os.getenv("GUNICORN_TIMEOUT", 30))

# Seconds to let running requests finish when the server stops or restarts.
graceful_timeout = 30

# Seconds to keep an idle connection open for the next request.
keepalive = 5

# Restart each worker after about 1000 requests, to keep memory use stable.
max_requests = 1000
max_requests_jitter = 100

# Write access and error logs to the terminal (or to journald under systemd).
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
