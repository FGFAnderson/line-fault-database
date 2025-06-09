from fastapi import FastAPI

from api.v1.routes import organisations, competition

app = FastAPI()
app.include_router(organisations.router)
app.include_router(competition.router)
