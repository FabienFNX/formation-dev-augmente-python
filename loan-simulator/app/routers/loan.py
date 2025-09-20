from fastapi import APIRouter, HTTPException
from typing import List

from app.models import LoanRequest, LoanResponse, CategoryInfo
from app.services.loan_service import loan_service
from app.services.interest_rate_client import interest_rate_client

router = APIRouter()


@router.post(
    "/calculate-loan",
    response_model=LoanResponse,
    summary="Calculer un prêt immobilier",
    description="Calcule les détails d'un prêt immobilier : mensualité, coût total des intérêts, etc. Supporte les interfaces client et employé.",
    responses={
        200: {"description": "Calcul du prêt réalisé avec succès"},
        400: {"description": "Données d'entrée invalides"},
        500: {"description": "Erreur interne du serveur"}
    }
)
async def calculate_loan(request: LoanRequest):
    try:
        response = await loan_service.calculate_loan(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@router.get(
    "/age-categories",
    response_model=List[CategoryInfo],
    summary="Obtenir les catégories d'âge",
    description="Retourne la liste des catégories d'âge disponibles pour l'interface employé",
    responses={
        200: {"description": "Liste des catégories d'âge récupérée avec succès"},
        500: {"description": "Erreur lors de la récupération des catégories"}
    }
)
async def get_age_categories():
    try:
        categories = await interest_rate_client.get_age_categories()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des catégories d'âge: {str(e)}")


@router.get(
    "/professional-categories",
    response_model=List[CategoryInfo],
    summary="Obtenir les catégories professionnelles",
    description="Retourne la liste des catégories professionnelles disponibles pour l'interface employé",
    responses={
        200: {"description": "Liste des catégories professionnelles récupérée avec succès"},
        500: {"description": "Erreur lors de la récupération des catégories"}
    }
)
async def get_professional_categories():
    try:
        categories = await interest_rate_client.get_professional_categories()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des catégories professionnelles: {str(e)}")