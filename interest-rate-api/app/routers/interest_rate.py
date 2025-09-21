from fastapi import APIRouter, HTTPException
from typing import List

from app.models import InterestRateRequest, InterestRateResponse, CategoryInfo
from app.services.interest_rate_service import interest_rate_service
from app.config import InterestRateConfig

router = APIRouter()


@router.post(
    "/interest-rate/calculate",
    response_model=InterestRateResponse,
    summary="Calculer le taux d'intérêt",
    description="Calcule le taux d'intérêt annuel en fonction de l'âge, de la catégorie professionnelle et du revenu mensuel",
    responses={
        200: {"description": "Taux d'intérêt calculé avec succès"},
        400: {"description": "Données d'entrée invalides"},
        500: {"description": "Erreur interne du serveur"}
    }
)
async def calculate_interest_rate(request: InterestRateRequest):
    try:
        response = interest_rate_service.calculate_interest_rate(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@router.get(
    "/interest-rate/categories/age",
    response_model=List[CategoryInfo],
    summary="Obtenir les catégories d'âge",
    description="Retourne la liste de toutes les catégories d'âge disponibles avec leurs modificateurs",
    responses={
        200: {"description": "Liste des catégories d'âge récupérée avec succès"}
    }
)
async def get_age_categories():
    return interest_rate_service.get_age_categories()


@router.get(
    "/interest-rate/categories/professional",
    response_model=List[CategoryInfo],
    summary="Obtenir les catégories professionnelles",
    description="Retourne la liste de toutes les catégories socio-professionnelles avec leurs modificateurs",
    responses={
        200: {"description": "Liste des catégories professionnelles récupérée avec succès"}
    }
)
async def get_professional_categories():
    return interest_rate_service.get_professional_categories()


@router.get(
    "/interest-rate/config",
    response_model=InterestRateConfig,
    summary="Obtenir la configuration actuelle",
    description="Retourne la configuration actuelle des taux et seuils utilisés pour les calculs",
    responses={
        200: {"description": "Configuration récupérée avec succès"}
    }
)
async def get_current_config():
    return interest_rate_service.get_current_config()