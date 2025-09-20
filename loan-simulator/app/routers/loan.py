from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models import (
    LoanRequest, LoanResponse, CategoryInfo,
    SaveSimulationRequest, SaveSimulationResponse, SimulationHistory
)
from app.services.loan_service import loan_service
from app.services.interest_rate_client import interest_rate_client
from app.services.simulation_service import simulation_service
from app.database import get_db

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


@router.post(
    "/save-simulation",
    response_model=SaveSimulationResponse,
    summary="Sauvegarder une simulation",
    description="Sauvegarde une simulation de prêt en base de données pour l'employé",
    responses={
        200: {"description": "Simulation sauvegardée avec succès"},
        400: {"description": "Données insuffisantes pour sauvegarder"},
        500: {"description": "Erreur lors de la sauvegarde"}
    }
)
async def save_simulation(request: SaveSimulationRequest, db: AsyncSession = Depends(get_db)):
    try:
        response = await simulation_service.save_simulation(request, db)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde: {str(e)}")


@router.get(
    "/simulation-history",
    response_model=List[SimulationHistory],
    summary="Historique des simulations",
    description="Récupère l'historique des simulations sauvegardées",
    responses={
        200: {"description": "Historique récupéré avec succès"},
        500: {"description": "Erreur lors de la récupération de l'historique"}
    }
)
async def get_simulation_history(limit: int = 50, db: AsyncSession = Depends(get_db)):
    try:
        history = await simulation_service.get_simulation_history(db, limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'historique: {str(e)}")


@router.get(
    "/simulation/{simulation_id}",
    response_model=SimulationHistory,
    summary="Détail d'une simulation",
    description="Récupère le détail d'une simulation par son ID",
    responses={
        200: {"description": "Simulation récupérée avec succès"},
        404: {"description": "Simulation non trouvée"},
        500: {"description": "Erreur lors de la récupération"}
    }
)
async def get_simulation_by_id(simulation_id: int, db: AsyncSession = Depends(get_db)):
    try:
        simulation = await simulation_service.get_simulation_by_id(simulation_id, db)
        return simulation
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")


# Additional endpoints for frontend compatibility

@router.get(
    "/saved-simulations",
    response_model=List[SimulationHistory],
    summary="Simulations sauvegardées (alias)",
    description="Alias pour /simulation-history - pour compatibilité frontend",
    responses={
        200: {"description": "Historique récupéré avec succès"},
        500: {"description": "Erreur lors de la récupération de l'historique"}
    }
)
async def get_saved_simulations(limit: int = 50, db: AsyncSession = Depends(get_db)):
    try:
        history = await simulation_service.get_simulation_history(db, limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'historique: {str(e)}")


@router.get(
    "/saved-simulations/{simulation_id}",
    response_model=SimulationHistory,
    summary="Détail d'une simulation sauvegardée (alias)",
    description="Alias pour /simulation/{id} - pour compatibilité frontend",
    responses={
        200: {"description": "Simulation récupérée avec succès"},
        404: {"description": "Simulation non trouvée"},
        500: {"description": "Erreur lors de la récupération"}
    }
)
async def get_saved_simulation_by_id(simulation_id: int, db: AsyncSession = Depends(get_db)):
    try:
        simulation = await simulation_service.get_simulation_by_id(simulation_id, db)
        return simulation
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")


@router.delete(
    "/saved-simulations/{simulation_id}",
    summary="Supprimer une simulation",
    description="Supprime une simulation par son ID",
    responses={
        200: {"description": "Simulation supprimée avec succès"},
        404: {"description": "Simulation non trouvée"},
        500: {"description": "Erreur lors de la suppression"}
    }
)
async def delete_simulation(simulation_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await simulation_service.delete_simulation(simulation_id, db)
        return {"message": "Simulation supprimée avec succès"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression: {str(e)}")