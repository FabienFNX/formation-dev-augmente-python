import math
from app.models import LoanRequest, LoanResponse


class LoanCalculationService:

    def calculate_loan(self, request: LoanRequest) -> LoanResponse:
        monthly_rate = request.annual_interest_rate / 100 / 12
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
            total_cost=round(total_cost, 2)
        )


loan_service = LoanCalculationService()