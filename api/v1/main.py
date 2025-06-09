from fastapi import FastAPI

from api.v1.routes import organisations

app = FastAPI()
app.include_router(organisations.router)
