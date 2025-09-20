from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.routers import loan
from app.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    await create_tables()
    yield


app = FastAPI(
    title="Loan Simulator",
    description="Simulateur de Prêt Immobilier - Frontend Application",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loan.router, prefix="/api", tags=["Loan Calculator"])

app.mount("/", StaticFiles(directory="loan-simulator/static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)