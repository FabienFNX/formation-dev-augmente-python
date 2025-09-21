from fastapi import APIRouter, HTTPException

from app.models import LoanRequest, LoanResponse
from app.services.loan_service import loan_service

router = APIRouter()


@router.post(
    "/calculate-loan",
    response_model=LoanResponse,
    summary="Calculer un prêt immobilier",
    description="Calcule les détails d'un prêt immobilier : mensualité, coût total des intérêts, etc.",
    responses={
        200: {"description": "Calcul du prêt réalisé avec succès"},
        400: {"description": "Données d'entrée invalides"},
        500: {"description": "Erreur interne du serveur"}
    }
)
async def calculate_loan(request: LoanRequest):
    try:
        response = loan_service.calculate_loan(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")