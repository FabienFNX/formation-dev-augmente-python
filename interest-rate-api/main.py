from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.routers import interest_rate
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Interest Rate API",
    description="API de calcul de taux d'intérêt basé sur des critères sociodémographiques",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/swagger-ui.html",
    openapi_url="/api-docs/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interest_rate.router, prefix="/api", tags=["Interest Rate"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)