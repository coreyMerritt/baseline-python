#!/usr/bin/env python3

from fastapi import FastAPI

from interfaces.rest.health.routes import health_routes
from interfaces.rest.v1.routes import account_routes

routers = FastAPI()
routers.include_router(health_routes.router)
routers.include_router(account_routes.router)
app = routers
