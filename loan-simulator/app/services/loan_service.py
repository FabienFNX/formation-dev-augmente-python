import math
from app.models import LoanRequest, LoanResponse
from app.services.interest_rate_client import interest_rate_client


class LoanCalculationService:

    async def calculate_loan(self, request: LoanRequest) -> LoanResponse:
        # Si les informations client sont fournies mais pas le taux, calculer automatiquement
        annual_interest_rate = request.annual_interest_rate

        if annual_interest_rate is None and self._is_employee_request(request):
            # Interface employé - calculer le taux automatiquement
            annual_interest_rate = await interest_rate_client.calculate_interest_rate(
                age_category=request.age_category,
                professional_category=request.professional_category,
                monthly_net_income=request.monthly_net_income
            )
        elif annual_interest_rate is None:
            raise ValueError("Le taux d'intérêt annuel est requis pour l'interface client")

        monthly_rate = annual_interest_rate / 100 / 12
        number_of_payments = request.duration_years * 12

        if monthly_rate == 0:
            monthly_payment = request.amount / number_of_payments
        else:
            monthly_payment = request.amount * (
                monthly_rate * (1 + monthly_rate) ** number_of_payments
            ) / (
                (1 + monthly_rate) ** number_of_payments - 1
            )

        total_cost = monthly_payment * number_of_payments
        total_interest = total_cost - request.amount

        return LoanResponse(
            loan_amount=round(request.amount, 2),
            monthly_payment=round(monthly_payment, 2),
            total_interest=round(total_interest, 2),
            total_cost=round(total_cost, 2),
            annual_interest_rate=round(annual_interest_rate, 2)
        )

    def _is_employee_request(self, request: LoanRequest) -> bool:
        """Détermine si c'est une requête de l'interface employé"""
        return (request.age_category is not None and
                request.professional_category is not None and
                request.monthly_net_income is not None)


loan_service = LoanCalculationService()