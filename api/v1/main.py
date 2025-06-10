from fastapi import FastAPI

from api.v1.routes import competitions, organisations, teams

app = FastAPI()
app.include_router(organisations.router)
app.include_router(competitions.router)
app.include_router(teams.router)
