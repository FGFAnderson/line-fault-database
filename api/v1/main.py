from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routes import (
    competitions,
    match,
    organisations,
    teams,
    set,
    elimination_event,
    throw_event,
)

app = FastAPI()

# RESTRICT THIS IN DEV TODO

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organisations.router)
app.include_router(competitions.router)
app.include_router(teams.router)
app.include_router(match.router)
app.include_router(set.router)
app.include_router(elimination_event.router)
app.include_router(throw_event.router)
