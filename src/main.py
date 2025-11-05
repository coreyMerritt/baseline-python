from fastapi import FastAPI
from interfaces.rest import routers

app: FastAPI | None = None

def create_app() -> FastAPI:
  global app
  if app is None:
    routers_module = routers
    app = routers_module.app
  return app
