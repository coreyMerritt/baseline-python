#!/usr/bin/env python3

# Handle configs before anything
# from infrastructure.config.config_manager import ConfigManager

# ConfigManager.refresh_configs()

from fastapi import FastAPI  # pylint: disable=wrong-import-position,wrong-import-order

from interfaces.rest.routes import account_routes  # pylint: disable=wrong-import-position

app = FastAPI()
app.include_router(account_routes.router)
