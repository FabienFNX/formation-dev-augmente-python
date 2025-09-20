from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import LoanSimulation
from app.models import SaveSimulationRequest, SaveSimulationResponse, SimulationHistory
from typing import List
from datetime import datetime


class SimulationService:

    async def save_simulation(self, request: SaveSimulationRequest, db: AsyncSession) -> SaveSimulationResponse:
        """Sauvegarde une simulation de prêt en base de données"""

        # Validation des données obligatoires
        loan_req = request.loan_request
        loan_resp = request.loan_response

        if not loan_req.first_name or not loan_req.last_name:
            raise ValueError("Le prénom et le nom sont obligatoires")

        if not loan_req.age_category or not loan_req.professional_category:
            raise ValueError("Les catégories d'âge et professionnelle sont obligatoires")

        # Créer l'enregistrement en base
        simulation = LoanSimulation(
            first_name=loan_req.first_name,
            last_name=loan_req.last_name,
            age_category=loan_req.age_category,
            professional_category=loan_req.professional_category,
            monthly_net_income=loan_req.monthly_net_income,
            loan_amount=loan_req.amount,
            duration_years=loan_req.duration_years,
            annual_interest_rate=loan_resp.annual_interest_rate,
            total_interest=loan_resp.total_interest,
            total_cost=loan_resp.total_cost,
            monthly_payment=loan_resp.monthly_payment,
            created_at=datetime.utcnow()
        )

        db.add(simulation)
        await db.commit()
        await db.refresh(simulation)

        return SaveSimulationResponse(
            id=simulation.id,
            message="Simulation sauvegardée avec succès"
        )

    async def get_simulation_history(self, db: AsyncSession, limit: int = 50) -> List[SimulationHistory]:
        """Récupère l'historique des simulations"""

        query = select(LoanSimulation).order_by(desc(LoanSimulation.created_at)).limit(limit)
        result = await db.execute(query)
        simulations = result.scalars().all()

        history = []
        for sim in simulations:
            history.append(SimulationHistory(
                id=sim.id,
                first_name=sim.first_name,
                last_name=sim.last_name,
                age_category=sim.age_category,
                professional_category=sim.professional_category,
                monthly_net_income=sim.monthly_net_income,
                loan_amount=sim.loan_amount,
                duration_years=sim.duration_years,
                annual_interest_rate=sim.annual_interest_rate,
                total_interest=sim.total_interest,
                total_cost=sim.total_cost,
                monthly_payment=sim.monthly_payment,
                created_at=sim.created_at.isoformat(),
                client_name=f"{sim.first_name} {sim.last_name}",
                formatted_created_at=sim.created_at.strftime("%d/%m/%Y à %H:%M")
            ))

        return history

    async def get_simulation_by_id(self, simulation_id: int, db: AsyncSession) -> SimulationHistory:
        """Récupère une simulation par son ID"""

        query = select(LoanSimulation).where(LoanSimulation.id == simulation_id)
        result = await db.execute(query)
        simulation = result.scalar_one_or_none()

        if not simulation:
            raise ValueError(f"Aucune simulation trouvée avec l'ID {simulation_id}")

        return SimulationHistory(
            id=simulation.id,
            first_name=simulation.first_name,
            last_name=simulation.last_name,
            age_category=simulation.age_category,
            professional_category=simulation.professional_category,
            monthly_net_income=simulation.monthly_net_income,
            loan_amount=simulation.loan_amount,
            duration_years=simulation.duration_years,
            annual_interest_rate=simulation.annual_interest_rate,
            total_interest=simulation.total_interest,
            total_cost=simulation.total_cost,
            monthly_payment=simulation.monthly_payment,
            created_at=simulation.created_at.isoformat(),
            client_name=f"{simulation.first_name} {simulation.last_name}",
            formatted_created_at=simulation.created_at.strftime("%d/%m/%Y à %H:%M")
        )

    async def delete_simulation(self, simulation_id: int, db: AsyncSession) -> None:
        """Supprime une simulation par son ID"""

        query = select(LoanSimulation).where(LoanSimulation.id == simulation_id)
        result = await db.execute(query)
        simulation = result.scalar_one_or_none()

        if not simulation:
            raise ValueError(f"Aucune simulation trouvée avec l'ID {simulation_id}")

        await db.delete(simulation)
        await db.commit()


simulation_service = SimulationService()