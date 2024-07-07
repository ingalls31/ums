import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from middleware.router_logging import RouterLoggingMiddleware
import src
from src.config.database import engine
from src.config.config import APP_NAME, logging_config, VERSION

import src.controllers
import src.controllers.users
from src.models import *
import src.models
import logging

logging.config.dictConfig(logging_config)

# from src.routes import users, auth

# from src.routes.users import main, models
# from src.routes.auth import main, models

src.models.users.Base.metadata.create_all(bind=engine)
# auth.models.Base.metadata.create_all(bind=engine)
# ----------------------------------------

app = FastAPI(
    title=APP_NAME,
    version=VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.add_middleware(
    RouterLoggingMiddleware,
    logger=logging.getLogger(__name__)
)

app.include_router(src.controllers.users.router)
# app.include_router(auth.main.router)
