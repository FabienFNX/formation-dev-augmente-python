from typing import List
from app.models import InterestRateRequest, InterestRateResponse, CategoryInfo, AgeCategory, ProfessionalCategory
from app.config import settings


class InterestRateCalculationService:

    def calculate_interest_rate(self, request: InterestRateRequest) -> InterestRateResponse:
        base_rate = settings.base_rate
        age_modifier = request.age_category.get_info()["rate_modifier"]
        professional_modifier = request.professional_category.get_info()["rate_modifier"]
        income_modifier = self._calculate_income_modifier(request.monthly_net_income)

        final_rate = base_rate + age_modifier + professional_modifier + income_modifier

        return InterestRateResponse(
            annual_interest_rate=round(final_rate, 2),
            base_rate=base_rate,
            age_modifier=age_modifier,
            professional_modifier=professional_modifier,
            income_modifier=income_modifier,
            age_category=request.age_category,
            professional_category=request.professional_category,
            monthly_net_income=request.monthly_net_income
        )

    def get_age_categories(self) -> List[CategoryInfo]:
        categories = []
        for category in AgeCategory:
            info = category.get_info()
            categories.append(CategoryInfo(
                name=category.value,
                description=info["description"],
                age_range=info["age_range"],
                rate_modifier=info["rate_modifier"]
            ))
        return categories

    def get_professional_categories(self) -> List[CategoryInfo]:
        categories = []
        for category in ProfessionalCategory:
            info = category.get_info()
            categories.append(CategoryInfo(
                name=info["name"],
                description=info["description"],
                rate_modifier=info["rate_modifier"]
            ))
        return categories

    def get_current_config(self):
        return settings

    def _calculate_income_modifier(self, monthly_income: float) -> float:
        thresholds = settings.income_thresholds

        if monthly_income < thresholds.low:
            return thresholds.low_modifier
        elif monthly_income < thresholds.medium:
            return thresholds.medium_modifier
        elif monthly_income < thresholds.high:
            return thresholds.high_modifier
        else:
            return thresholds.very_high_modifier


interest_rate_service = InterestRateCalculationService()