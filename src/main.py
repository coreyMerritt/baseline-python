#!/usr/bin/env python3

from fastapi import FastAPI

from interfaces.rest.routes import account_routes


app = FastAPI()
app.include_router(account_routes.router)

