from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
import os

# Database configuration
DATABASE_URL = "sqlite+aiosqlite:///./loan_simulator.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session maker
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()


class LoanSimulation(Base):
    __tablename__ = "loan_simulations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age_category = Column(String, nullable=False)
    professional_category = Column(String, nullable=False)
    monthly_net_income = Column(Float, nullable=False)
    loan_amount = Column(Float, nullable=False)
    duration_years = Column(Integer, nullable=False)
    annual_interest_rate = Column(Float, nullable=False)
    total_interest = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    monthly_payment = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)