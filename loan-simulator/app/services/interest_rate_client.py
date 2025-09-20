import httpx
import asyncio
from typing import List, Optional
from app.models import CategoryInfo


class InterestRateClient:
    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url
        self.timeout = 10.0

    async def get_age_categories(self) -> List[CategoryInfo]:
        """Récupère les catégories d'âge depuis l'API Interest Rate"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/api/interest-rate/categories/age")
                response.raise_for_status()

                categories_data = response.json()
                categories = []

                for cat_data in categories_data:
                    categories.append(CategoryInfo(
                        code=cat_data["code"],  # Enum value for API calls
                        name=cat_data["description"],
                        description=cat_data.get("age_range", ""),
                        rate_modifier=cat_data["rate_modifier"]
                    ))

                return categories
            except httpx.RequestError as e:
                raise Exception(f"Erreur de connexion à l'API Interest Rate: {e}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Erreur HTTP lors de la récupération des catégories d'âge: {e.response.status_code}")

    async def get_professional_categories(self) -> List[CategoryInfo]:
        """Récupère les catégories professionnelles depuis l'API Interest Rate"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/api/interest-rate/categories/professional")
                response.raise_for_status()

                categories_data = response.json()
                categories = []

                for cat_data in categories_data:
                    categories.append(CategoryInfo(
                        code=cat_data["code"],  # Enum value for API calls
                        name=cat_data["name"],
                        description=cat_data["description"],
                        rate_modifier=cat_data["rate_modifier"]
                    ))

                return categories
            except httpx.RequestError as e:
                raise Exception(f"Erreur de connexion à l'API Interest Rate: {e}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Erreur HTTP lors de la récupération des catégories professionnelles: {e.response.status_code}")

    async def calculate_interest_rate(self, age_category: str, professional_category: str, monthly_net_income: float) -> float:
        """Calcule le taux d'intérêt via l'API Interest Rate"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                request_data = {
                    "age_category": age_category,
                    "professional_category": professional_category,
                    "monthly_net_income": monthly_net_income
                }

                response = await client.post(
                    f"{self.base_url}/api/interest-rate/calculate",
                    json=request_data
                )
                response.raise_for_status()

                result = response.json()
                return result["annual_interest_rate"]

            except httpx.RequestError as e:
                raise Exception(f"Erreur de connexion à l'API Interest Rate: {e}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Erreur HTTP lors du calcul du taux d'intérêt: {e.response.status_code}")


# Instance globale du client
interest_rate_client = InterestRateClient()