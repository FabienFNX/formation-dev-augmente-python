from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class AgeCategory(str, Enum):
    YOUNG_ADULT = "YOUNG_ADULT"
    ADULT = "ADULT"
    MIDDLE_AGED = "MIDDLE_AGED"
    SENIOR = "SENIOR"

    def get_info(self):
        info_map = {
            "YOUNG_ADULT": {"age_range": "18-30 ans", "description": "Jeune adulte", "rate_modifier": 0.2},
            "ADULT": {"age_range": "31-45 ans", "description": "Adulte", "rate_modifier": 0.0},
            "MIDDLE_AGED": {"age_range": "46-60 ans", "description": "Âge moyen", "rate_modifier": -0.1},
            "SENIOR": {"age_range": "61+ ans", "description": "Senior", "rate_modifier": 0.3}
        }
        return info_map[self.value]


class ProfessionalCategory(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    EXECUTIVE = "EXECUTIVE"
    CIVIL_SERVANT = "CIVIL_SERVANT"
    FREELANCER = "FREELANCER"
    RETIRED = "RETIRED"
    STUDENT = "STUDENT"
    UNEMPLOYED = "UNEMPLOYED"

    def get_info(self):
        info_map = {
            "EMPLOYEE": {"name": "Salarié CDI", "description": "Employé en contrat à durée indéterminée", "rate_modifier": 0.0},
            "EXECUTIVE": {"name": "Cadre", "description": "Cadre dirigeant ou ingénieur", "rate_modifier": -0.2},
            "CIVIL_SERVANT": {"name": "Fonctionnaire", "description": "Agent de la fonction publique", "rate_modifier": -0.3},
            "FREELANCER": {"name": "Indépendant", "description": "Travailleur indépendant ou freelance", "rate_modifier": 0.4},
            "RETIRED": {"name": "Retraité", "description": "Personne à la retraite", "rate_modifier": 0.1},
            "STUDENT": {"name": "Étudiant", "description": "Étudiant ou apprenti", "rate_modifier": 0.5},
            "UNEMPLOYED": {"name": "Sans emploi", "description": "Personne sans activité professionnelle", "rate_modifier": 0.8}
        }
        return info_map[self.value]


class CategoryInfo(BaseModel):
    name: str
    description: str
    age_range: Optional[str] = None
    rate_modifier: float


class InterestRateRequest(BaseModel):
    age_category: AgeCategory = Field(..., description="Catégorie d'âge du demandeur")
    professional_category: ProfessionalCategory = Field(..., description="Catégorie socio-professionnelle")
    monthly_net_income: float = Field(..., gt=0, description="Revenu mensuel net en euros")

    class Config:
        json_schema_extra = {
            "example": {
                "age_category": "ADULT",
                "professional_category": "EMPLOYEE",
                "monthly_net_income": 3500.0
            }
        }


class InterestRateResponse(BaseModel):
    annual_interest_rate: float = Field(..., description="Taux d'intérêt annuel calculé en pourcentage")
    base_rate: float = Field(..., description="Taux de base utilisé")
    age_modifier: float = Field(..., description="Modificateur appliqué pour l'âge")
    professional_modifier: float = Field(..., description="Modificateur appliqué pour la catégorie professionnelle")
    income_modifier: float = Field(..., description="Modificateur appliqué pour le revenu")
    age_category: AgeCategory = Field(..., description="Catégorie d'âge utilisée")
    professional_category: ProfessionalCategory = Field(..., description="Catégorie professionnelle utilisée")
    monthly_net_income: float = Field(..., description="Revenu mensuel net considéré")

    class Config:
        json_schema_extra = {
            "example": {
                "annual_interest_rate": 1.7,
                "base_rate": 1.5,
                "age_modifier": 0.2,
                "professional_modifier": 0.0,
                "income_modifier": 0.0,
                "age_category": "ADULT",
                "professional_category": "EMPLOYEE",
                "monthly_net_income": 3500.0
            }
        }