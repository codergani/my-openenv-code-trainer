# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

"""
FastAPI application for the My Assistant Bot Environment.

This module creates an HTTP server that exposes the MyAssistantBotEnvironment
over HTTP and WebSocket endpoints, compatible with EnvClient.

Endpoints:
    - POST /reset: Reset the environment
    - POST /step: Execute an action
    - GET /state: Get current environment state
    - GET /schema: Get action/observation schemas
    - WS /ws: WebSocket endpoint for persistent sessions

Usage:
    # Development (with auto-reload):
    uvicorn server.app:app --reload --host 0.0.0.0 --port 8000

    # Production:
    uvicorn server.app:app --host 0.0.0.0 --port 8000 --workers 4

    # Or run directly:
    python -m server.app
"""

try:
    from openenv.core.env_server.http_server import create_app
except Exception as e:  # pragma: no cover
    raise ImportError(
        "openenv is required for the web interface. Install dependencies with '\n    uv sync\n'"
    ) from e

try:
    from my_assistant_bot.models import MyAssistantBotAction, MyAssistantBotObservation
    from my_assistant_bot.server.my_assistant_bot_environment import MyAssistantBotEnvironment
except (ImportError, ValueError):
    try:
        from ..models import MyAssistantBotAction, MyAssistantBotObservation
        from .my_assistant_bot_environment import MyAssistantBotEnvironment
    except (ImportError, ValueError):
        from models import MyAssistantBotAction, MyAssistantBotObservation
        from server.my_assistant_bot_environment import MyAssistantBotEnvironment


# Enable the web interface by default
os.environ.setdefault("ENABLE_WEB_INTERFACE", "true")

# Create the app with web interface and README integration
app = create_app(
    MyAssistantBotEnvironment,
    MyAssistantBotAction,
    MyAssistantBotObservation,
    env_name="my_assistant_bot",
    max_concurrent_envs=1,  # increase this number to allow more concurrent WebSocket sessions
)


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

# Mount the premium static UI
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/elite", include_in_schema=False)
async def serve_elite_ui():
    """Serve the premium dashboard."""
    return FileResponse(static_path / "index.html")

@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect root to the elite UI."""
    return RedirectResponse(url="/elite")


def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")

if __name__ == '__main__':
    main()
