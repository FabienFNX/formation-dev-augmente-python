from pydantic import BaseModel, Field


class LoanRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Montant du prêt en euros")
    duration_years: int = Field(..., gt=0, alias="durationYears", description="Durée du prêt en années")
    annual_interest_rate: float = Field(..., ge=0, alias="annualInterestRate", description="Taux d'intérêt annuel en pourcentage")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "amount": 250000.0,
                "durationYears": 20,
                "annualInterestRate": 1.7
            }
        }


class LoanResponse(BaseModel):
    loan_amount: float = Field(..., alias="loanAmount", description="Montant emprunté")
    monthly_payment: float = Field(..., alias="monthlyPayment", description="Mensualité")
    total_interest: float = Field(..., alias="totalInterest", description="Coût total des intérêts")
    total_cost: float = Field(..., alias="totalCost", description="Coût total du prêt")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "loanAmount": 250000.0,
                "monthlyPayment": 1289.25,
                "totalInterest": 59420.0,
                "totalCost": 309420.0
            }
        }