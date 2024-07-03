from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.config.database import engine
from src.config.config import APP_NAME, VERSION


from src.routes import users, auth

from src.routes.users import main, models
from src.routes.auth import main, models

users.models.Base.metadata.create_all(bind=engine)
auth.models.Base.metadata.create_all(bind=engine)
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

app.include_router(users.main.router)
app.include_router(auth.main.router)
