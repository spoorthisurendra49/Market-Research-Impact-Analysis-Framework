from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Market Intelligence AI")
app.include_router(router)
