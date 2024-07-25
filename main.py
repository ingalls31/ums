import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

import src.controllers.classes
import src.controllers.departments
import src.controllers.majors
import src.controllers.points
import src.controllers.students
import src.controllers.subjects
import src.controllers.teachers
from src.middleware.router_logging import RouterLoggingMiddleware
import src
from src.config.settings import engine
from src.config.config import APP_NAME, logging_config, VERSION

import src.controllers
import src.controllers.users
from src.models import *
import src.models
import logging

import src.models.classes
import src.models.departments
import src.models.majors
import src.models.points
import src.models.subjects
import src.models.users

logging.config.dictConfig(logging_config)

src.models.users.Base.metadata.create_all(bind=engine)
src.models.subjects.Base.metadata.create_all(bind=engine)
src.models.classes.Base.metadata.create_all(bind=engine)
src.models.points.Base.metadata.create_all(bind=engine)
src.models.departments.Base.metadata.create_all(bind=engine)
src.models.majors.Base.metadata.create_all(bind=engine)
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
app.include_router(src.controllers.students.router)
app.include_router(src.controllers.teachers.router)
app.include_router(src.controllers.subjects.router)
app.include_router(src.controllers.classes.router)
app.include_router(src.controllers.points.router)
app.include_router(src.controllers.departments.router)
app.include_router(src.controllers.majors.router)
# app.include_router(auth.main.router)
