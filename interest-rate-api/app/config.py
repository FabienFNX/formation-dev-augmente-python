from pydantic import BaseModel
from typing import Dict


class IncomeThresholds(BaseModel):
    low: float = 2000.0
    medium: float = 4000.0
    high: float = 8000.0
    low_modifier: float = 0.3
    medium_modifier: float = 0.0
    high_modifier: float = -0.1
    very_high_modifier: float = -0.2


class InterestRateConfig(BaseModel):
    base_rate: float = 1.5
    income_thresholds: IncomeThresholds = IncomeThresholds()


settings = InterestRateConfig()