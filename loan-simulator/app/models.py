from pydantic import BaseModel, Field
from typing import Optional


class LoanRequest(BaseModel):
    # Client information (for employee interface)
    first_name: Optional[str] = Field(None, alias="firstName", description="Prénom du client")
    last_name: Optional[str] = Field(None, alias="lastName", description="Nom du client")
    age_category: Optional[str] = Field(None, alias="ageCategory", description="Catégorie d'âge")
    professional_category: Optional[str] = Field(None, alias="professionalCategory", description="Catégorie professionnelle")
    monthly_net_income: Optional[float] = Field(None, alias="monthlyNetIncome", description="Revenu mensuel net")

    # Loan parameters
    amount: float = Field(..., gt=0, description="Montant du prêt en euros")
    duration_years: int = Field(..., gt=0, alias="durationYears", description="Durée du prêt en années")
    annual_interest_rate: Optional[float] = Field(None, ge=0, alias="annualInterestRate", description="Taux d'intérêt annuel en pourcentage")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "amount": 250000.0,
                "durationYears": 20,
                "annualInterestRate": 1.7
            }
        }


class CategoryInfo(BaseModel):
    code: str = Field(..., description="Code de la catégorie")
    name: str = Field(..., description="Nom de la catégorie")
    description: str = Field(..., description="Description de la catégorie")
    rate_modifier: float = Field(..., alias="rateModifier", description="Modificateur de taux")

    class Config:
        populate_by_name = True


class LoanResponse(BaseModel):
    loan_amount: float = Field(..., alias="loanAmount", description="Montant emprunté")
    monthly_payment: float = Field(..., alias="monthlyPayment", description="Mensualité")
    total_interest: float = Field(..., alias="totalInterest", description="Coût total des intérêts")
    total_cost: float = Field(..., alias="totalCost", description="Coût total du prêt")
    annual_interest_rate: Optional[float] = Field(None, alias="annualInterestRate", description="Taux d'intérêt annuel appliqué")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "loanAmount": 250000.0,
                "monthlyPayment": 1289.25,
                "totalInterest": 59420.0,
                "totalCost": 309420.0,
                "annualInterestRate": 1.7
            }
        }


class SaveSimulationRequest(BaseModel):
    loan_request: LoanRequest = Field(..., alias="loanRequest", description="Données de la demande de prêt")
    loan_response: LoanResponse = Field(..., alias="loanResponse", description="Résultats du calcul de prêt")

    class Config:
        populate_by_name = True


class SaveSimulationResponse(BaseModel):
    id: int = Field(..., description="ID de la simulation sauvegardée")
    message: str = Field(..., description="Message de confirmation")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 123,
                "message": "Simulation sauvegardée avec succès"
            }
        }


class SimulationHistory(BaseModel):
    id: int
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    age_category: str = Field(..., alias="ageCategory")
    professional_category: str = Field(..., alias="professionalCategory")
    monthly_net_income: float = Field(..., alias="monthlyNetIncome")
    loan_amount: float = Field(..., alias="loanAmount")
    duration_years: int = Field(..., alias="durationYears")
    annual_interest_rate: float = Field(..., alias="annualInterestRate")
    total_interest: float = Field(..., alias="totalInterest")
    total_cost: float = Field(..., alias="totalCost")
    monthly_payment: float = Field(..., alias="monthlyPayment")
    created_at: str = Field(..., alias="createdAt")

    # Additional fields for frontend compatibility
    client_name: str = Field(..., alias="clientName", description="Nom complet du client")
    formatted_created_at: str = Field(..., alias="formattedCreatedAt", description="Date formatée pour affichage")

    class Config:
        populate_by_name = True
        from_attributes = True